from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, CurriculumForm, ExperienciaLaboralForm, EducacionForm, HabilidadForm, ReferenciaForm
from .models import Curriculum, Usuario, ExperienciaLaboral, Educacion, Habilidad, Referencia
from weasyprint import HTML
from django.template.loader import render_to_string
import stripe
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Plantilla  # Asegúrate de que la ruta sea correcta




# Configuración de la clave de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Vista de inicio
def index(request):
    return render(request, 'curriculum/index.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, request.FILES)  # Agregar request.FILES para la imagen
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registration/registro.html', {'usuario_form': usuario_form})

# Vista para el inicio de sesión
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

# Vista para crear un currículum
@login_required
def crear_curriculum(request):
    if request.method == 'POST':
        # Solo se procesan los formularios de currículum y sus secciones
        curriculum_form = CurriculumForm(request.POST, request.FILES)
        experiencia_form = ExperienciaLaboralForm(request.POST)
        educacion_form = EducacionForm(request.POST)
        habilidad_form = HabilidadForm(request.POST)
        referencia_form = ReferenciaForm(request.POST)

        # Validamos todos los formularios
        if (curriculum_form.is_valid() and 
            experiencia_form.is_valid() and 
            educacion_form.is_valid() and 
            habilidad_form.is_valid() and 
            referencia_form.is_valid()):

            # Guardamos el currículum
            curriculum = curriculum_form.save(commit=False)
            curriculum.usuario = request.user  # Asignamos el usuario autenticado
            curriculum.save()

            # Guardamos las secciones relacionadas
            for form, model in [(experiencia_form, ExperienciaLaboral), 
                                (educacion_form, Educacion), 
                                (habilidad_form, Habilidad), 
                                (referencia_form, Referencia)]:
                instance = form.save(commit=False)
                instance.curriculum = curriculum
                instance.save()

            return redirect('curriculum_detalle', curriculum_id=curriculum.pk)

    else:
        # Inicializamos solo los formularios necesarios
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

# Vista para ver un currículum
@login_required
def ver_curriculum(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    return render(request, 'cv_template_1.html', {
        'curriculum': curriculum,
    })

# Vista para agregar experiencia a un currículum
@login_required
def agregar_experiencia(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
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

# Vista para mostrar los detalles de un currículum
@login_required
def curriculum_detalle(request, curriculum_id):
    # Obtenemos el currículum por su ID
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)

    # Verificamos que el currículum pertenece al usuario autenticado
    if curriculum.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este currículum.")

    # Obtenemos todas las secciones del currículum
    experiencias = curriculum.experiencias.all()
    educaciones = curriculum.educaciones.all()
    habilidades = curriculum.habilidades.all()
    referencias = curriculum.referencias.all()

    # Preparamos el contexto para enviar a la plantilla
    context = {
        'curriculum': curriculum,
        'usuario': curriculum.usuario,
        'experiencias': experiencias,
        'educaciones': educaciones,
        'habilidades': habilidades,
        'referencias': referencias,
    }

    # Renderizamos la plantilla con los detalles del currículum
    return render(request, 'curriculum/cv_template_1.html', context)




# Vista para mostrar la lista de plantillas
@login_required
def lista_plantillas(request):
    if request.user.es_premium:
        plantillas = Plantilla.objects.all()
    else:
        plantillas = Plantilla.objects.filter(es_premium=False)

    return render(request, 'lista_plantillas.html', {'plantillas': plantillas})

# Vista para generar un currículum en formato HTML
def generar_cv_1(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    experiencias = ExperienciaLaboral.objects.filter(curriculum__usuario=usuario)
    educacion = Educacion.objects.filter(curriculum__usuario=usuario)
    habilidades = Habilidad.objects.filter(curriculum__usuario=usuario)

    context = {
        'usuario': usuario,
        'experiencias': experiencias,
        'educacion': educacion,
        'habilidades': habilidades,
    }
    return render(request, 'curriculum/cv_template_1.html', context)

# Vista para descargar el currículum en formato PDF
def descargar_cv_1(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    curriculum = Curriculum.objects.filter(usuario=usuario).first()
    
    # Manejo de caso donde no hay currículum
    if curriculum is None:
        return HttpResponse("El usuario no tiene currículum disponible.", status=404)

    experiencias = ExperienciaLaboral.objects.filter(curriculum=curriculum)
    educaciones = Educacion.objects.filter(curriculum=curriculum)
    habilidades = Habilidad.objects.filter(curriculum=curriculum)
    referencias = Referencia.objects.filter(curriculum=curriculum)

    context = {
        'usuario': usuario,
        'curriculum': curriculum,
        'experiencias': experiencias,
        'educaciones': educaciones,
        'habilidades': habilidades,
        'referencias': referencias,
    }

    html = render_to_string('cv_template_1.html', context)
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="curriculum.pdf"'
    return response

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin



# Vista para manejar los cargos de Stripe
class ChargeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'payment/charge.html', {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,  # Solo la clave pública aquí
        })

    def post(self, request):
        amount = 100  # en centavos (1 USD)
        currency = 'usd'
        
        # Configura la clave secreta solo aquí
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            stripe.Charge.create(
                amount=amount,
                currency=currency,
                description="Acceso premium a plantillas de CV",
                source=request.POST['stripeToken']
            )
            request.user.es_premium = True
            request.user.save()
            return redirect('charge_success')
        
        except stripe.error.CardError as e:
            return render(request, 'payment/charge_failed.html', {'error': str(e)})