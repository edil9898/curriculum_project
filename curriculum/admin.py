from django.contrib import admin
from .models import Usuario, Curriculum, ExperienciaLaboral, Educacion, Habilidad, Referencia

admin.site.register(Usuario)
admin.site.register(Curriculum)
admin.site.register(ExperienciaLaboral)
admin.site.register(Educacion)
admin.site.register(Habilidad)
admin.site.register(Referencia)
