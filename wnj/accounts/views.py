from django.shortcuts import render

def sign_up(request):
    return render(request, 'accounts/account_sign_up.html')
