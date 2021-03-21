from django.shortcuts import render
from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def es_fiscal(user):
    return user.groups.filter(name='Fiscalizador').exists()

@login_required
@user_passes_test(es_fiscal)
def clienteIndex(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}

    return render(request, 'appremoto/fiscal_index.html', context)