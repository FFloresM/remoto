from django.shortcuts import render
from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

def es_fiscal(user):
    return user.groups.filter(name='Fiscalizador').exists()

@login_required
@user_passes_test(es_fiscal)
def clienteIndex(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }

    return render(request, 'appremoto/fiscal_index.html', context)

@login_required
@user_passes_test(es_fiscal)
def predios(request, pk):
    cliente = Cliente.objects.get(id=pk)
    predios = Predio.objects.filter(cliente_id=pk)
    predios = list(predios)
    pilas = Pila.objects.filter(cliente_id=pk)
    context = {
        'predios': predios,
        'cliente': cliente,
        'pilas': pilas,
    }

    return render(request, 'appremoto/predios_cliente.html', context)

@login_required
def home(request):
    return render(request, 'appremoto/welcome.html' )
    