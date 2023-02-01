
from django.urls import path
from .views import home,index


urlpatterns = [
    path('', index),
    path('home/', home),
]
