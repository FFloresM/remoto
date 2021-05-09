import io
from django.http import FileResponse
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from reportlab.lib import colors
from .models import *
from .forms import *
from .pdftezt import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
#para rest
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewd or edited
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewd or edited
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
	""" API endpoint para clientes """
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializer
	permission_classes = [permissions.IsAuthenticated]

class CuentaUsuarioViewSet(viewsets.ModelViewSet):
	""" API endpoint para cuentausuario"""
	queryset = CuentaUsuario.objects.all()
	serializer_class = CuentaUsuarioSerializer
	permission_classes = [permissions.IsAuthenticated]

class LanzaViewSet(viewsets.ModelViewSet):
	""" API endpoint para Lanza"""
	queryset = Lanza.objects.all()
	serializer_class = LanzaSerializer
	permission_classes = [permissions.IsAuthenticated]

class PilaViewSet(viewsets.ModelViewSet):
	""" API endpoint para Pila"""
	queryset = Pila.objects.all()
	serializer_class = PilaSerializer
	permission_classes = [permissions.IsAuthenticated]

class MedicionViewSet(viewsets.ModelViewSet):
	""" API endpoint para Medicion"""
	queryset = Medicion.objects.all()
	serializer_class = MedicionSerializer
	permission_classes = [permissions.IsAuthenticated]

class MateriaPrimaViewSet(viewsets.ModelViewSet):
	""" API endpoint para MateriaPrima"""
	queryset = MateriaPrima.objects.all()
	serializer_class = MateriaPrimaSerializer
	permission_classes = [permissions.IsAuthenticated]

class PredioViewSet(viewsets.ModelViewSet):
	""" API endpoint para Predio"""
	queryset = Predio.objects.all()
	serializer_class = PredioSerializer
	permission_classes = [permissions.IsAuthenticated]

#vistas de la app
@login_required()
def index(request):
	cu = CuentaUsuario.objects.get(usuario=request.user)
	cliente = cu.cliente
	lanzas = Lanza.objects.filter(cliente=cliente)
	pilas = Pila.objects.filter(cliente=cliente)
	context = {
		'cliente': cliente,
		'lanzas': lanzas,
		'pilas': pilas,
	}
	return render(request, 'app/index.html', context)

class PilaCreate(LoginRequiredMixin, CreateView):
	model = Pila
	form_class = PilaCreateForm

	def get_success_url(self):
		return reverse('app:index')

class PilaDelete(LoginRequiredMixin, DeleteView):
	model = Pila
	success_url = reverse_lazy('app:index')

class PilaUpdate(LoginRequiredMixin, UpdateView):
	model = Pila
	form_class = PilaUpdateForm
	template_name = 'app/pila_update.html'
	success_url = reverse_lazy('app:index')

class MateriaPrimaCreate(LoginRequiredMixin, CreateView):
	model = MateriaPrima
	form_class = MateriaPrimaCreateForm
	success_url = reverse_lazy('app:index')

class PredioCreate(LoginRequiredMixin, CreateView):
	model = Predio
	fields = ['nombre']
	success_url = reverse_lazy('app:index')

@login_required()
def medicionesPila(request, pk):
	pila = Pila.objects.get(id=pk)
	query = Medicion.objects.filter(pila=pila)
	last_foto = query[len(query)-1].foto if len(query) else None
	materia_prima = MateriaPrima.objects.filter(pila=pila)
	context = {
		'registros': query,
		'pila': pila,
		'foto': last_foto,
		'materia_prima': materia_prima,
	}
	return render(request, 'app/mediciones_pila.html', context)
	


class RegistrosView(LoginRequiredMixin, generic.ListView):
	model = Medicion
	context_object_name = 'mediciones'
	#nueva consulta
	#queryset = Medicion.objects.filter()
	template_name = 'app/registros.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cu = CuentaUsuario.objects.get(usuario=self.request.user)
		context['now'] = timezone.now()
		context['pilas'] = Pila.objects.filter(cliente=cu.cliente)
		return context

@login_required()
def chart(request, pk):
	mediciones = Medicion.objects.filter(pila__id=pk)
	pila = Pila.objects.get(id=pk)
	temps = mediciones.values_list('temperatura', flat=True)
	dates = mediciones.values_list('fecha_creacion', flat=True)
	dias = [i for i in range(1,len(dates)+1) ]
	_55 = [55 for i in dias]
	humedad = mediciones.values_list('humedad', flat=True)
	context = {
		'pila': pila,
		'temps': list(temps),
		'dias': dias,
		'dates': dates,
		'humedad': list(humedad),
		'FF': _55,
	}
	return render(request, 'app/chart_pila.html', context)

@login_required()
def allCharts(request):
	cu = CuentaUsuario.objects.get(usuario=request.user)
	cliente = cu.cliente
	pilas = Medicion.objects.filter(pila__cliente=cliente).values_list('pila', flat=True).distinct().order_by()
	temps = {}
	hum = {}
	color = {}
	R = 255
	for p in pilas:
		p_ID = Pila.objects.get(id=p)
		med = Medicion.objects.filter(pila_id=p)
		temps[p_ID.nombreID] = list(med.values_list('temperatura', flat=True))
		color['borderColor'] = f"rgb({R},0,0)"
		hum[p_ID.nombreID] = list(med.values_list('humedad', flat=True))
		R=R-20
	#dias = [i for i in range(1,len(dates)+1) ]
	_55 = [55]*10
	context = {
		'temps': temps,
		'hum': hum,
		'FF': _55,
	}
	return render(request, 'app/chart.html', context)

@login_required()
def pdf_test(request, pk):
	#queries for models
	mediciones_ = Medicion.objects.filter(pila__id=pk)
	mediciones = mediciones_.values_list()
	last_foto = mediciones_[len(mediciones_)-1].foto
	pila = Pila.objects.get(id=pk)
	cliente = Cliente.objects.get(id=pila.cliente_id)
	lanza = Lanza.objects.get(cliente=cliente)
	materiaprima = MateriaPrima.objects.filter(pila = pila).values_list()
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()
	hoy = datetime.today()
	#datos y funciones para generar pdf
	title = f"Reporte Pila {pila.nombreID}"
	setTitle(title)
	pageinfo = f"pila-{pila.nombreID}/{cliente.nombre}/{lanza.numero_serie}/"+hoy.strftime("%H:%M/%d-%m-%y")
	setPageInfo(pageinfo)
	if last_foto:
		setDataFirstTable(cliente, lanza, last_foto.file.name)
	else:
		setDataFirstTable(cliente, lanza, None)
	setDetallePila(pila)
	setMateriasPrimas(materiaprima)
	setDataMediciones(mediciones)
	humedad = list(mediciones.values_list('humedad', flat=True))
	for v,h in enumerate(humedad):
		humedad[v] = (v+1,h)
	setHumedad(tuple(humedad))
	temps = list(mediciones.values_list('temperatura', flat=True))
	for v,t in enumerate(temps):
		temps[v] = (v+1,t)
	setTemps(tuple(temps))
	
	# Create the PDF object, using the buffer as its "file."
	go(buffer)

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	#nombre de reporte
	
	return FileResponse(buffer, as_attachment=False, filename='reporte.pdf')
