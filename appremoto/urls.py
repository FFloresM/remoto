from appremoto.views import clienteIndex, predios
from django.urls import path
from app.views import *

app_name = 'appremoto'

urlpatterns = [
    path('', clienteIndex, name='clienteIndex'),
    path('predios/<int:pk>', predios, name='predios'),
]