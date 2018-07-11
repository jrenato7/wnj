from django.shortcuts import render

from wnj.accounts.forms import AccountSignUpForm


def sign_up(request):
    context = {'form': AccountSignUpForm()}
    return render(request, 'accounts/account_sign_up.html', context)
