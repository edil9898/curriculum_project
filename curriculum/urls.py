from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import ChargeView
from django.contrib.auth import views as auth_views  # Asegúrate de importar auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('registro/', views.registro, name='registro'),  # Página de registro
    path('login/', views.login_view, name='login'),  # Página de inicio de sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Cerrar sesión
    path('crear_curriculum/', views.crear_curriculum, name='crear_curriculum'),  # Crear currículum
    path('curriculum/<int:curriculum_id>/', views.curriculum_detalle, name='curriculum_detalle'),  # Detalles del currículum
    path('plantillas/', views.lista_plantillas, name='lista_plantillas'),
    path('curriculum/<int:curriculum_id>/agregar_experiencia/', views.agregar_experiencia, name='agregar_experiencia'),  # Añadir experiencia
    path('<int:usuario_id>/cv_1/', views.generar_cv_1, name='generar_cv_1'),
    path('<int:usuario_id>/cv_1/descargar/', views.descargar_cv_1, name='descargar_cv_1'), 
    path('charge/', ChargeView.as_view(), name='charge'),  # Página de carga
    path('charge/success/', TemplateView.as_view(template_name='payment/charge_success.html'), name='charge_success'),  # Éxito de carga
] 
if settings.DEBUG:  # Asegúrate de que esta parte solo esté activa en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
