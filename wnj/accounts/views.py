from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from wnj.accounts.forms import RegisterForm
from wnj.accounts.models import User


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'])
            user.set_password(form.cleaned_data['password2'])
            user.save()
            messages.success(request, 'Success! You can log in now.')
            return HttpResponseRedirect('/signup/')
        else:
            return render(
                request, 'accounts/signup.html', {'form': form})

    context = {'form': RegisterForm()}
    return render(request, 'accounts/signup.html', context)
