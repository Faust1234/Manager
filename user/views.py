from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Userregistarions, UserUpdateForm, ProfileUpdateForm


def index(request):
    return render(request, 'user/index.html')

def register(request):
    if request.method == 'POST':
        form = Userregistarions(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You log in')
            return redirect('login')


    else:
        form = Userregistarions()

    return render(request, 'user/register.html', {'form': form})

@login_required #just for test
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'user/profile.html', context)


