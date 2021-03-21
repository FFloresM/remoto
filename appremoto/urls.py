from appremoto.views import clienteIndex
from django.urls import path
from app.views import *

app_name = 'appremoto'

urlpatterns = [
    path('', clienteIndex, name='clienteIndex'),
]