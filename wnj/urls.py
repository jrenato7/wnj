"""wnj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import login, logout

from wnj.core.views import home
from wnj.accounts.views import sign_up
from wnj.galleries.views import gallery, moments, add_picture


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('signup/', sign_up),
    path('login/', login),
    path('logout/', logout),
    path('gallery/', gallery),
    path('moments/', moments),
    path('add_picture/', add_picture),
]
