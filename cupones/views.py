import os
import uuid 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from supabase import create_client, Client

from .models import Cupon, Recuerdo
from .forms import RecuerdoForm

# Aquí están tus llaves de conexión a Supabase ✨
SUPABASE_URL = "https://obvktqnikkqelwwfziqi.supabase.co" 
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
            # Esperamos antes de guardar
            recuerdo = form.save(commit=False)
            
            # Obtenemos la foto
            foto_fisica = request.FILES.get('imagen')

            if foto_fisica:
                # 1. Nos conectamos a Supabase
                supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

                # 2. Creamos nombre único
                extension = foto_fisica.name.split('.')[-1]
                nombre_unico = f"foto_{uuid.uuid4()}.{extension}"

                # 3. Leemos la foto
                foto_bytes = foto_fisica.read()

                # 4. ¡La subimos al Bucket "fotos"!
                supabase.storage.from_("fotos").upload(
                    file=foto_bytes,
                    path=nombre_unico,
                    file_options={"content-type": foto_fisica.content_type}
                )

                # 5. Pedimos el link público de la cajita "fotos"
                url_magica = supabase.storage.from_("fotos").get_public_url(nombre_unico)

                # 6. Guardamos el enlace en Django
                recuerdo.imagen = url_magica

            # ¡Ahora sí, guardamos en la base de datos!
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