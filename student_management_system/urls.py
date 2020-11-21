"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import *
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, HttpResponse

def index(request):

    #业务逻辑

    #返回请求

    #return HttpResponse('index')
    return render(request,'index.html')#返回html页面

def login(request):
    return render(request,'login.html')

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('index/',index)
]
