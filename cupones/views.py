import os
import uuid 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from supabase import create_client, Client

from .models import Cupon, Recuerdo
from .forms import RecuerdoForm

# Configuración de Supabase
SUPABASE_URL = "https://obvktqnikkqelwwfziqi.supabase.co" 
# REEMPLAZA ESTO por tu clave 'service_role' de Supabase (empieza por eyJ...)
SUPABASE_KEY = "sb_publishable_hr77xjMbgfuMCbThrMmuAg_FTyHE4ej" 

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
            recuerdo = form.save(commit=False)
            foto_fisica = request.FILES.get('imagen')

            if foto_fisica:
                # 1. Nos conectamos con la llave de superpoderes
                supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

                # 2. Creamos nombre único
                extension = foto_fisica.name.split('.')[-1]
                nombre_unico = f"foto_{uuid.uuid4()}.{extension}"

                # 3. Subimos al bucket "fotos"
                supabase.storage.from_("fotos").upload(
                    file=foto_fisica.read(),
                    path=nombre_unico,
                    file_options={"content-type": foto_fisica.content_type}
                )

                # 4. Construimos la URL pública manualmente para mayor seguridad
                url_magica = f"{SUPABASE_URL}/storage/v1/object/public/fotos/{nombre_unico}"
                
                # 5. Guardamos el enlace completo en Django
                recuerdo.imagen = url_magica

            recuerdo.save()
            return redirect('lista_recuerdos')
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

