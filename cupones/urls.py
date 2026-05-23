from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.index, name='index'),

    # 💜 Cupones
    path('cupones/canjear/<int:cupon_id>/', views.canjear_cupon, name='canjear_cupon'),

    # 🌸 Recuerdos
    path('recuerdos/', views.lista_recuerdos, name='lista_recuerdos'),
    path('recuerdos/nuevo/', views.crear_recuerdo, name='crear_recuerdo'),
    path('recuerdos/<int:id>/', views.detalle_recuerdo, name='detalle_recuerdo'),
]