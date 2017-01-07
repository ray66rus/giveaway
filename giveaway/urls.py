from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^list$', views.list, name='list'),
        url(r'^find_clients$', views.find_clients, name='find_clients'),
    ]
