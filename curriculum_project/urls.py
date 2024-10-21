# curriculum_project/urls.py (archivo principal del proyecto)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('curriculum.urls')),  # Incluir las URLs de la aplicación 'curriculum'
    path('accounts/', include('django.contrib.auth.urls')),  # Incluir rutas de autenticación (login, logout)
]
