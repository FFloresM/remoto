from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    fecha_creacion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Cliente
        fields = '__all__'

class CuentaUsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuentaUsuario
        fields = ['usuario', 'cliente']

class LanzaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lanza
        fields = '__all__'

class PilaSerializer(serializers.HyperlinkedModelSerializer):
    fecha_creacion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Pila
        fields = '__all__'

class MedicionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medicion
        fields = '__all__'

class MateriaPrimaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MateriaPrima
        fields = '__all__'

class PredioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Predio
        fields = '__all__'