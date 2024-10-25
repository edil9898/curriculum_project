from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('registro/', views.registro, name='registro'),  # Página de registro
    path('login/', views.login_view, name='login'),  # Página de inicio de sesión
    path('logout/', views.logout_view, name='logout'),  # Cerrar sesión
    path('crear_curriculum/', views.crear_curriculum, name='crear_curriculum'),  # Crear currículum
    path('curriculum/<int:curriculum_id>/', views.curriculum_detalle, name='curriculum_detalle'),  # Detalles del currículum
    path('curriculum/<int:curriculum_id>/agregar_experiencia/', views.agregar_experiencia, name='agregar_experiencia'),  # Añadir experiencia
    path('<int:usuario_id>/cv_1/', views.generar_cv_1, name='generar_cv_1'),
    path('<int:usuario_id>/cv_1/descargar/', views.descargar_cv_1, name='descargar_cv_1'), 
]

