from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^list$', views.list, name='list'),
        url(r'^client_giveaways/(?P<pk>\w*)/$', views.client_giveaways, name='client_giveaways'),
        url(r'^giveaways_list/(?P<client_id>\w*)/$', views.giveaways_list_by_client, name='client_giveaways_list'),
        url(r'^find_clients$', views.find_clients, name='find_clients'),
        url(r'^client/add/$', views.CreateClientView.as_view(), name='client_add'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
