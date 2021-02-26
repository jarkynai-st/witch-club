from django.contrib import admin
from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('',homepage,name='home'),
    path('signin/',sign_in,name='login'),
    path('create_order/<int:product_id>/',create_order,name='create_order'),
    path('contacts/', contacts_page, name='contacts'),
    path('logout', logout_page, name='logout'),
    path('signup/', sign_up, name='register'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]

