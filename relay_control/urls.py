from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trigger/', views.trigger_relay, name='trigger_relay'),
]