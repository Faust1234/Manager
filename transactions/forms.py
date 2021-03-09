from django import forms
from django.forms import ModelForm
from .models import Transaction
from categories.models import Category
from django.contrib.admin.widgets import AdminDateWidget
from .choices import *


class DateInput(forms.DateInput):
    input_type = 'date'

class TransactoinForms(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    operation_type = forms.ChoiceField(choices=OPERATIONS_CHOICES, required=True)
    pub_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Transaction
        fields = ['category', 'operation_type', 'money', 'description', 'pub_date']

    def __init__(self, user=None, **kwargs):
        super(TransactoinForms, self).__init__(**kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

