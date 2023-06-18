"""w3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from w import views
from w3 import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='reg'),
    url(r'^home/', views.home, name='home'),
    url(r'^vip/', views.vip, name='vip'),
    url(r'^exhibit/', views.exhibit, name='exhibit'),
    url(r'^set_password/', views.set_password, name='set_pwd'),
    url(r'^set_avatar/', views.set_avatar, name='set_ava'),
    url(r'^backend/', views.backend, name='backend'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^shop_car/', views.shop_car),
    url(r'^up_or_down/', views.up_or_down),
    url(r'^comment/', views.comment),
    url(r'^pay/', views.pay),
    url(r'^cancel/', views.cancel),
    url(r'^add/goods/', views.add_goods, name='add_goods'),
    url(r'^(?P<username>\w+)/$', views.site, name='site'),
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/', views.site),
    url(r'^(?P<username>\w+)/goods/(?P<goods_id>\d+)/', views.goods_detail),
]