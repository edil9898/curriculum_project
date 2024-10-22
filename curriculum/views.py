from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, CurriculumForm, ExperienciaLaboralForm, EducacionForm, HabilidadForm, ReferenciaForm
from .models import Curriculum, Usuario

def index(request):
    return render(request, 'curriculum/index.html')

# Vista para el registro de usuarios
from .forms import UsuarioForm  # Importa el formulario personalizado

def registro(request):
    # ... código de la vista

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registration/registro.html', {'usuario_form': usuario_form})

def login_view(request):
    if request.method == 'POST':
        correo_electronico = request.POST['correo_electronico']
        contrasena = request.POST['contrasena']
        try:
            user = Usuario.objects.get(correo_electronico=correo_electronico)
        except Usuario.DoesNotExist:
            error_message = "Correo o contraseña incorrectos"
            return render(request, 'registration/login.html', {'error_message': error_message})

        if user is not None and user.check_password(contrasena):
            login(request, user)
            return redirect('crear_curriculum')
        else:
            error_message = "Correo o contraseña incorrectos"
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')

# Vista para el cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def crear_curriculum(request):
    if request.method == 'POST':
        curriculum_form = CurriculumForm(request.POST)
        experiencia_form = ExperienciaLaboralForm(request.POST)
        educacion_form = EducacionForm(request.POST)
        habilidad_form = HabilidadForm(request.POST)
        referencia_form = ReferenciaForm(request.POST)

        if curriculum_form.is_valid() and experiencia_form.is_valid() and educacion_form.is_valid() and habilidad_form.is_valid() and referencia_form.is_valid():
            # Obtener el usuario actual
            usuario = request.user

            curriculum = curriculum_form.save(commit=False)
            curriculum.usuario = usuario
            curriculum.save()

            experiencia = experiencia_form.save(commit=False)
            experiencia.curriculum = curriculum
            experiencia.save()

            educacion = educacion_form.save(commit=False)
            educacion.curriculum = curriculum
            educacion.save()

            habilidad = habilidad_form.save(commit=False)
            habilidad.curriculum = curriculum
            habilidad.save()

            referencia = referencia_form.save(commit=False)
            referencia.curriculum = curriculum
            referencia.save()

            return redirect('curriculum_detalle', curriculum_id=curriculum.pk)
    else:
        curriculum_form = CurriculumForm()
        experiencia_form = ExperienciaLaboralForm()
        educacion_form = EducacionForm()
        habilidad_form = HabilidadForm()
        referencia_form = ReferenciaForm()

    return render(request, 'crear_curriculum.html', {
        'curriculum_form': curriculum_form,
        'experiencia_form': experiencia_form,
        'educacion_form': educacion_form,
        'habilidad_form': habilidad_form,
        'referencia_form': referencia_form,
    })

# Vista para agregar experiencia laboral (solo si está autenticado)
@login_required
def agregar_experiencia(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    # Verificar si el usuario actual es el propietario del currículum
    if curriculum.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este currículum.") 

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
    # Verificar si el usuario actual es el propietario del currículum
    if curriculum.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este currículum.")
    return render(request, 'curriculum_detalle.html', {'curriculum': curriculum})