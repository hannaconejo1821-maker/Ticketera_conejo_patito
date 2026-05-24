from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.split),
    path('', include('cupones.urls')), 
]

# ¡ESTA ES LA LÍNEA MÁGICA!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Esto ayuda a que Render pueda servir los archivos subidos directamente de forma temporal
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)