from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    contrasena = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Curriculum(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    plantilla_seleccionada = models.CharField(max_length=100)
    formato_exportacion = models.CharField(max_length=100)
     

    def __str__(self):
        return f"Curriculum de {self.usuario.nombre} ({self.fecha_creacion})"

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
