# curriculum_project/urls.py (archivo principal del proyecto)
from django.contrib import admin
from django.urls import path, include
from curriculum import views  # Importa el módulo views de tu aplicación curriculum
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('curriculum.urls')),  # Incluir las URLs de la aplicación 'curriculum'
    path('accounts/', include('django.contrib.auth.urls')),  # Incluir rutas de autenticación (login, logout)
    path('cv1/<int:usuario_id>/', views.generar_cv_1, name='generar_cv_1'),
    


] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)