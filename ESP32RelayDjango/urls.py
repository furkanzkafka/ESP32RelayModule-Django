from django.urls import path, include

urlpatterns = [
    path('', include('relay_control.urls')),
]