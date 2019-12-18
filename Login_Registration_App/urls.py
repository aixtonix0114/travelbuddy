from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('logout', views.logout),
    path('add', views.addpage),
    path('addplan', views.addplan),
    path('travels/destination/<other_id>', views.destInfo),
    path('travels/<other_id>', views.jointrip),
]
