"""ArticleBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index2/', views.index2),
    path('about/', views.about),
    path('listpic/', views.listpic),
    path('newslistpic/', views.newslistpic),
    re_path('newslistpic/(?P<type>\w+)/(?P<page>\d+)', views.newslistpic),
    path('base/', views.base),
    re_path('articledetails/(?P<id>\d+)', views.articledetails),
    path('addarticle/', views.addarticle),
    path('fytest/', views.fytest),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path("formtest/",views.formtest),
    path("formtest2/",views.formtest2),
    path("reqtest/",views. reqtest),
    path("register/",views.register),
    path("register2/",views.register2),
    path("register3/",views.register3),
    path("register4/",views.register4),
    path("cspost/",views.cspost),


    path("ajax_get/",views.ajax_get),
    path("ajax_get_data/",views.ajax_get_data),
    path("ajax_post/",views.ajax_post),
    path('ajax_post_data/',views.ajax_post_data),
    path("checkusername/",views.checkusername),
    path("login/",views.login),
    path("logout/",views.logout),

   path("Article/",include("Article.urls")),
]




