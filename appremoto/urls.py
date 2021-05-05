from appremoto.views import clienteIndex, predios, home
from django.urls import path
from app.views import *

app_name = 'appremoto'

urlpatterns = [
    path('index/', clienteIndex, name='clienteIndex'),
    path('predios/<int:pk>', predios, name='predios'),
    path('', home, name='home')
]