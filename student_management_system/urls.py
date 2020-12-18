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
from api import views

admin.autodiscover()

urlpatterns = [
    path('', views.user_login),
    path('admin/', admin.site.urls),
    path('login/', views.user_login),
    path('index/', views.index),
    # path('department_list/', views.department_list),
    # path('department_add/', views.department_add),
    # path('department_del/', views.department_del),
    # path('department_edit/', views.department_edit),
    # path('course_list/', views.course_list),
    # path('course_add/', views.course_add),
    path('course_del/', views.course_del),
    path('student_elective/', views.student_elective),
    path('elect_course/', views.elect_course),
    path('self_course/', views.self_course),
    path('self_information/', views.self_information),
    path('user_logout/', views.user_logout),
    path('history_course/', views.history_course),
    path('export_users_csv/', views.export_users_csv),
    path('export_users_xls/', views.export_users_xls),
    path('teacher_management/', views.teacher_management),
    path('score_edit/', views.score_edit),
    path('teacher_course/', views.teacher_course),
    path('teacher_information/', views.teacher_information),
    path('my_students/', views.my_students),
    path('export_students_csv/', views.export_students_csv),
    path('export_students_xls/', views.export_students_csv),
    path('retake_course/', views.retake_course),
]
