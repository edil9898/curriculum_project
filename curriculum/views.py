from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, CurriculumForm, ExperienciaLaboralForm, EducacionForm, HabilidadForm, ReferenciaForm
from .models import Curriculum

def index(request):
    return render(request, 'curriculum/index.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')  # Redirige al login después del registro exitoso
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registration/registro.html', {'usuario_form': usuario_form})

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        correo_electronico = request.POST['correo_electronico']
        contrasena = request.POST['contrasena']
        user = authenticate(request, username=correo_electronico, password=contrasena)
        if user is not None:
            login(request, user)
            return redirect('crear_curriculum')  # Redirige a la creación del currículum después de iniciar sesión
        else:
            error_message = "Correo o contraseña incorrectos"
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')

# Vista para el cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión

# Vista para la creación del currículum (solo accesible si está autenticado)
@login_required
def crear_curriculum(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        curriculum_form = CurriculumForm(request.POST)

        if usuario_form.is_valid() and curriculum_form.is_valid():
            usuario = usuario_form.save()
            curriculum = curriculum_form.save(commit=False)
            curriculum.usuario = usuario
            curriculum.save()
            return redirect('curriculum_detalle', curriculum_id=curriculum.pk)  # Corrige el nombre de la variable aquí
    else:
        usuario_form = UsuarioForm()
        curriculum_form = CurriculumForm()

    return render(request, 'crear_curriculum.html', {
        'usuario_form': usuario_form,
        'curriculum_form': curriculum_form,
    })

# Vista para agregar experiencia laboral (solo si está autenticado)
@login_required
def agregar_experiencia(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    if request.method == 'POST':
        experiencia_form = ExperienciaLaboralForm(request.POST)
        if experiencia_form.is_valid():
            experiencia = experiencia_form.save(commit=False)
            experiencia.curriculum = curriculum
            experiencia.save()
            return redirect('curriculum_detalle', curriculum_id=curriculum_id)
    else:
        experiencia_form = ExperienciaLaboralForm()
    return render(request, 'agregar_experiencia.html', {'experiencia_form': experiencia_form})

# Vista para mostrar los detalles del currículum (solo si está autenticado)
@login_required
def curriculum_detalle(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    return render(request, 'curriculum_detalle.html', {'curriculum': curriculum})
