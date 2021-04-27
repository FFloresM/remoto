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
	materia_prima = MateriaPrima.objects.filter(pila=pila)
	context = {
		'registros': query,
		'pila': pila,
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
	dias = [date.day for date in dates ]
	humedad = mediciones.values_list('humedad', flat=True)
	context = {
		'pila': pila,
		'temps': list(temps),
		'dias': dias,
		'dates': dates,
		'humedad': list(humedad),
	}
	return render(request, 'app/chart_pila.html', context)

@login_required()
def allCharts(request):
	mediciones = Medicion.objects.all()
	context = {
		'mediciones': mediciones,
	}
	return render(request, 'app/chart.html', context)

@login_required()
def pdf_test(request, pk):
	#queries for models
	mediciones = Medicion.objects.filter(pila__id=pk).values_list()
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
	setDataFirstTable(cliente, lanza, pila.foto.file.name)
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
