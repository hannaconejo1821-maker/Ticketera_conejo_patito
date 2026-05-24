from django.db import models


class Cupon(models.Model):

    titulo = models.CharField(max_length=100)

    descripcion = models.TextField()

    imagen = models.CharField(max_length=255)

    disponible = models.BooleanField(default=True)

    fecha_canje = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo

class Recuerdo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    # 👇 Cambiamos ImageField por CharField
    # Le ponemos 500 de espacio porque las URLs a veces son largas
    imagen = models.CharField(max_length=500, null=True, blank=True)
    
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo