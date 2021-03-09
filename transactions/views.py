from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
)
from categories.models import Category
from .choices import *
from .models import Transaction
from .forms import TransactoinForms
import json

class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_create.html'
    form_class = TransactoinForms

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
        context['form'] = TransactoinForms(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/all_transaction.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        transaction = request.POST['transaction']
        category = Category.objects.get(name=transaction, user=self.request.user)
        object_list = Transaction.objects.filter(category=category, user=self.request.user)
        context = {
            'object_list': object_list,
            'category_list': Category.objects.filter(user=self.request.user),
        }
        return render(request, self.template_name, context)


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/delete_transaction.html'
    success_url = '/'

    def test_func(self):
        category = self.get_object()

        if self.request.user == category.user:
            return True
        else:
            return False


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'transactions/transaction_create.html'
    form_class = TransactoinForms
    queryset = Transaction.objects.all()

    def test_func(self):
        transaction = self.get_object()

        if self.request.user == transaction.user:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)


def generate_spline(request):

    choices = [i[0] for i in OPERATIONS_CHOICES]
    context = {
        'option_list': choices,
        'categories_list': Category.objects.filter(user=request.user),
    }
    if request.method == 'POST':
        try:
            start = request.POST['start']
            end = request.POST['end']
            option = request.POST['option']
            category = request.POST['category']
            category = Category.objects.get(name=category, user=request.user)
            data = Transaction.objects.filter(user=request.user, category=category, operation_type=option, pub_date__range=(start, end))
            data_for_graph = [[i.pub_date.strftime('%Y-%m-%d'), float(i.money)] for i in data]
            print(data_for_graph)
            context['data'] = json.dumps(data_for_graph)
            context['operation'] = option
        except:
            messages.warning(request, 'You should select date!')
            return redirect('spline')

    return render(request, 'transactions/spline_graph.html', context)


def generate_pie(request):

    choices = [i[0] for i in OPERATIONS_CHOICES]
    context = {
        'option_list': choices,
    }
    if request.method == 'POST':
        try:
            start = request.POST['start']
            end = request.POST['end']
            option = request.POST['option']
            data = Transaction.objects.filter(user=request.user, operation_type=option, pub_date__range=(start, end))
            categories = Category.objects.filter(user=request.user)
            data_for_graph = []
            for category in categories:
                data_for_graph.append({'name': category.name, 'y': sum([float(i.money) for i in data.filter(category=category)])})

            print(data_for_graph)
            context['data'] = json.dumps(data_for_graph)
            context['data_for_table'] = data_for_graph
            context['operation'] = option
            context['start'] = start
            context['end'] = end
        except:
            messages.warning(request, 'You should select date!')
            return redirect('pie')

    return render(request, 'transactions/pie_graph.html', context)