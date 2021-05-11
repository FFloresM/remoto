from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    """ Empresa o agricultor que compra la lanza"""
    #id automatico con autoincremento
    nombre = models.CharField(max_length=200, default="")
    rut = models.CharField(max_length=9)
    direccion = models.CharField(max_length=200, default="")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, default="")
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)

    def __str__(self):
        if self.nombre:
            return self.nombre
        return self.rut

    class Meta:
        ordering = ('nombre', )

class CuentaUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username + " de " + self.cliente.nombre
    
    class Meta:
        ordering = ('usuario',)
        verbose_name_plural = "Cuentas de Usuario"
    


class Lanza(models.Model):
    """Instrumento de medición"""
    codigo = models.CharField(max_length=100, unique=True, null=False)
    numero_serie = models.CharField("numero de serie", max_length=100, unique=True, null=False)
    modelo = models.CharField(max_length=20, default="")
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.cliente.nombre}"

class Pila(models.Model):
    """Pila"""
    nombreID = models.CharField(max_length=10, default=None)
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, null=True)
    posicion = models.CharField(max_length=20, null=True) #solo para prubas
    predio = models.ForeignKey('Predio', on_delete=models.SET_NULL, null=True)
    visitado = models.BooleanField(default=False)

    def __str__(self):
    	return f"{self.nombreID} - {self.cliente.nombre}"

    def estado_actual(self):
        temps = self.medicion_set.values_list('temperatura', flat=True)
        if temps:
            if len(list(filter(lambda i:i<=45, temps))) > 1:
                return "Fase I: mesófila"
            elif len(list(filter(lambda i:i>45, temps))) > 7:
                return 'Fase II: termófila'
            elif len(list(filter(lambda i:i<=45, temps))) >= 28:
                return 'Fase III: enfriamiento'
            elif len(temps) >= 35 and len(list(filter(lambda i:i<=45, temps))) >= 28:
                return 'Fase IV: maduración'
            else:
                return "indeterminado"
        else:
            return "Pila sin registros"

    class Meta:
        ordering = ('cliente', )

class Medicion(models.Model):
    """Datos que son medidos por la lanza"""
    fecha_creacion = models.DateTimeField("fecha de creacion", auto_now_add=True)
    temperatura = models.IntegerField(default=0)
    humedad = models.IntegerField(null=True)
    foto = models.ImageField(upload_to='Fotos', null=True, blank=True) #folder Fotos
    lanza = models.ForeignKey('Lanza', on_delete=models.DO_NOTHING)
    pila = models.ForeignKey('Pila', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fecha_creacion.strftime("%d-%m-%Y")
    
    class Meta:
        verbose_name_plural = 'Mediciones'
        ordering = ('fecha_creacion', )

class MateriaPrima(models.Model):
    """Materias primas utilizadas en el compost"""
    nombre = models.CharField(max_length=100, null=False)
    cantidad = models.IntegerField(null=False)
    unidad_medida = models.CharField(max_length=10, null=True)
    pila = models.ForeignKey('Pila', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Materias Primas'
        ordering = ('nombre', )

class Predio(models.Model):
    """Toda pila pertenece a un predio"""
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.nombre