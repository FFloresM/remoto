from django.contrib import admin
from .models import *
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'email', 'direccion')

class CuentaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cliente')

class LanzaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'modelo', 'cliente')

class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pila')

class MedicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperatura', 'humedad', 'pila')

class PilaAdmin(admin.ModelAdmin):
    list_display = ('nombreID', 'predio', 'cliente')

class PredioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente')
    
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Lanza, LanzaAdmin)
admin.site.register(Pila, PilaAdmin)
admin.site.register(Medicion, MedicionAdmin)
admin.site.register(MateriaPrima, MateriaPrimaAdmin)
admin.site.register(Predio, PredioAdmin)
admin.site.register(CuentaUsuario, CuentaUsuarioAdmin)