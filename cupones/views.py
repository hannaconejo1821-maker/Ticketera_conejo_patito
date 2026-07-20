import os
import uuid 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required # 🔑 ¡El candado de Django!
from supabase import create_client, Client
from dotenv import load_dotenv # 👈 Importamos la librería para el archivo .env

from .models import Cupon, Recuerdo
from .forms import RecuerdoForm

# 👈 Le decimos a Python que cargue los secretos del archivo .env local
load_dotenv() 

# Configuración segura de Supabase (¡Ya no están en texto plano!)
SUPABASE_URL = os.environ.get("SUPABASE_URL") 
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@login_required # 🔒 Obliga a loguearse para ver la app
def index(request):
    cupones = Cupon.objects.filter(disponible=True)
    # 🎟️ ¡Ordenados por fecha de canje! (El menos '-' hace que el más reciente salga primero)
    historial = Cupon.objects.filter(disponible=False).order_by('-fecha_canje')
    recuerdos = Recuerdo.objects.all().order_by('-fecha')

    return render(request, 'cupones/index.html', {
        'cupones': cupones,
        'historial': historial,
        'recuerdos': recuerdos
    })

@login_required
def canjear_cupon(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    cupon.disponible = False
    cupon.fecha_canje = timezone.now()
    cupon.save()

    return redirect('index')

@login_required
def crear_recuerdo(request):
    if request.method == 'POST':
        form = RecuerdoForm(request.POST, request.FILES)
        
        if form.is_valid():
            recuerdo = form.save(commit=False)
            foto_fisica = request.FILES.get('imagen')

            if foto_fisica:
                supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                extension = foto_fisica.name.split('.')[-1]
                nombre_unico = f"foto_{uuid.uuid4()}.{extension}"

                supabase.storage.from_("fotos").upload(
                    file=foto_fisica.read(),
                    path=nombre_unico,
                    file_options={"content-type": foto_fisica.content_type}
                )

                url_magica = f"{SUPABASE_URL}/storage/v1/object/public/fotos/{nombre_unico}"
                recuerdo.imagen = url_magica

            recuerdo.save()
            return redirect('lista_recuerdos')
    else:
        form = RecuerdoForm()

    return render(request, 'cupones/crear_recuerdo.html', {
        'form': form
    })

@login_required
def lista_recuerdos(request):
    recuerdos = Recuerdo.objects.all().order_by('-fecha')
    return render(request, 'cupones/lista_recuerdos.html', {
        'recuerdos': recuerdos
    })

@login_required
def detalle_recuerdo(request, id):
    # 👇 ¡Aquí está el arreglo del error NameError que tenías antes!
    recuerdo = get_object_or_404(Recuerdo, id=id) 
    
    return render(request, 'cupones/detalle_recuerdo.html', {
        'recuerdo': recuerdo
    })