from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  
    
    # 🔑 ¡Añadimos esta línea! Activa /accounts/login/ y /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('', include('cupones.urls')),
]

# Esto sirve para que se vean las fotos que subas
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)