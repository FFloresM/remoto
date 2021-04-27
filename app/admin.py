from django.contrib import admin
from .models import *
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'email', 'direccion')

class CuentaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cliente')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Lanza)
admin.site.register(Pila)
admin.site.register(Medicion)
admin.site.register(MateriaPrima)
admin.site.register(Predio)
admin.site.register(CuentaUsuario, CuentaUsuarioAdmin)