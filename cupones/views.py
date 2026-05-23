from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Cupon, Recuerdo
from .forms import RecuerdoForm


def index(request):
    cupones = Cupon.objects.filter(disponible=True)
    historial = Cupon.objects.filter(disponible=False)
    recuerdos = Recuerdo.objects.all().order_by('-fecha')

    return render(request, 'cupones/index.html', {
        'cupones': cupones,
        'historial': historial,
        'recuerdos': recuerdos
    })


def canjear_cupon(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    cupon.disponible = False
    cupon.fecha_canje = timezone.now()
    cupon.save()

    return redirect('index')


def crear_recuerdo(request):
    if request.method == 'POST':
        form = RecuerdoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_recuerdos')  # 👈 IMPORTANTE
    else:
        form = RecuerdoForm()

    return render(request, 'cupones/crear_recuerdo.html', {
        'form': form
    })


def lista_recuerdos(request):
    recuerdos = Recuerdo.objects.all().order_by('-fecha')

    return render(request, 'cupones/lista_recuerdos.html', {
        'recuerdos': recuerdos
    })


def detalle_recuerdo(request, id):
    recuerdo = get_object_or_404(Recuerdo, id=id)

    return render(request, 'cupones/detalle_recuerdo.html', {
        'recuerdo': recuerdo
    })