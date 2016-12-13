"""AAcms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from step1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^online/regist/$',views.regist,name='regist'),
    url(r'^online/login/$',views.login,name='login'),
    url(r'^online/index/$',views.index,name='index'),
    url(r'^online/logout/$',views.logout,name='logout'),
    url(r'^online/userinfo/$',views.userinfo,name='userinfo'),
    url(r'^online/createact/$',views.createact,name='createact'),
    url(r'^online/actinfo/(\d+)/$', views.actinfo, name='actinfo'),
]
