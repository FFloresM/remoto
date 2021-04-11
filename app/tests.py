from app.models import Cliente
from django.test import TestCase

# Create your tests here.
class ClienteTestCase(TestCase):
    def setUp(self):
        Cliente.objects.create(nombre='Gabriel', rut = '23456746', email='asd@13.com')
        Cliente.objects.create(nombre='El Compost Ltda.', rut = '694567891', email='asddd@567.cl')

    def test_cliente_tiene_nombre(self):
        cliente1 = Cliente.objects.get(nombre = 'Gabriel')
        cliente2 = Cliente.objects.get(nombre = 'El Compost Ltda.')
        self.assertEqual(cliente1.nombre, 'Gabriel')
        self.assertEqual(cliente2.rut, '694567891')