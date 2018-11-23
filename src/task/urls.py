from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^callback/$', views.CallBack.as_view(), name='callback'),
    url(r'^logout/$', views.MyLogoutView.as_view(), name='logout'),
    url(r'^login/$', views.MyLoginView.as_view(), name='login'),
    url(r'^tweets/$', views.TweetsView.as_view(), name='tweets'),
]
