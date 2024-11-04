from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    es_premium = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_curriculum',  # Agrega related_name aquí
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_curriculum',  # Agrega related_name aquí
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    

    def __str__(self):
        return self.username
        
class Curriculum(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    plantilla_seleccionada = models.CharField(max_length=100)
    formato_exportacion = models.CharField(max_length=100)

    nombres = models.CharField(max_length=100, blank=True, null=True)  # Campo para Nombres
    apellidos = models.CharField(max_length=100, blank=True, null=True)  # Campo para Apellidos
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Campo para Teléfono
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Campo para Dirección
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
    
    

    def __str__(self):
        return f"Curriculum de {self.usuario.username} ({self.fecha_creacion})"  # Usa 'username'
    
    from django.db import models

class Plantilla(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la plantilla
    descripcion = models.TextField(blank=True)  # Descripción de la plantilla
    es_premium = models.BooleanField(default=False)  # Indica si es una plantilla premium
    imagen = models.ImageField(upload_to='plantillas/')  # Imagen de vista previa de la plantilla
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    actualizado_en = models.DateTimeField(auto_now=True)  # Fecha de la última actualización

    def __str__(self):
        return self.nombre


class ExperienciaLaboral(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name="experiencias")
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

class Educacion(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name="educaciones")
    institucion = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()

    def __str__(self):
        return f"{self.titulo} en {self.institucion}"

class Habilidad(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name="habilidades")
    nombre_habilidad = models.CharField(max_length=100)
    nivel_competencia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_habilidad

class Referencia(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name="referencias")
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    telefono = models.CharField(max_length=15)
    parentesco = models.CharField(max_length=100)

    def __str__(self):
        return f"Referencia: {self.nombre}"