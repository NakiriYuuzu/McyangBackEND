"""mcyang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from sql_test.views import delete,get_id,index,update,login
from database_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database_api.urls')),
    # path('',index),
    # path('delete/<int:article_id>',delete),
    # path('get_id/<int:id>',get_id),
    # path('update/',update)



]
