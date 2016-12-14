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
<<<<<<< HEAD
from . import settings
from django.conf.urls.static import static
=======
>>>>>>> 54f479e04df4510eab85bffd66fffe40d274ff2b

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^online/login/$',views.login,name='login'),
    url(r'^online/index/$',views.index,name='index'),
    url(r'^online/logout/$',views.logout,name='logout'),
    url(r'^online/userinfo/$',views.userinfo,name='userinfo'),
    url(r'^online/actinfo/(\d+)/$', views.actinfo, name='actinfo'),
    url(r'^online/userinfo_new/$',views.userinfo_new,name='userinfo_new'),
<<<<<<< HEAD
    url(r'^online/actinfo_new/(\d+)/$', views.actinfo_new, name='actinfo_new'),
    url(r'^online/add_action/$',views.add_action,name='add_action'),
    url(r'^online/add_action_f/$',views.add_action_f,name='add_action_f'),
    url(r'^online/tping/$',views.tping,name='tping'),
    url(r'^online/add_status/$',views.add_status,name='add_status'),
   #url(r'^online/actinfo_new/', views.index, name='actinfo_new2'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
=======
]



>>>>>>> 54f479e04df4510eab85bffd66fffe40d274ff2b
