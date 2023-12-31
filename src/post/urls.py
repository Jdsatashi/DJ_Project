from django.urls import path
from .views import *

app_name = 'post'


urlpatterns = [
    path('', index, name='index'),
    path('create', create, name='create'),
    path('update/<slug>', update, name='update'),
    path('delete/<slug>', delete, name='delete'),
]
