from django import forms
from .models import Usuario
from .models import Curriculum, ExperienciaLaboral, Educacion, Habilidad, Referencia
from django.contrib.auth.forms import UserCreationForm

PLANTILLAS_CHOICES = [
    ('plantilla_1', 'Plantilla 1'),
    ('plantilla_2', 'Plantilla 2'),
    # ... añade más opciones si las tienes
]



class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email')  # Incluye los campos que necesitas

    email = forms.EmailField(label="Correo electrónico")  # Campo para el correo electrónico
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])  # Establece la contraseña de forma segura
        if commit:
            user.save()
        return user
    
    
# Formulario para la creación del Curriculum
class CurriculumForm(forms.ModelForm):
    plantilla_seleccionada = forms.ChoiceField(choices=PLANTILLAS_CHOICES)

    class Meta:
        model = Curriculum
        fields = ['plantilla_seleccionada', 'formato_exportacion']

# Formulario para la experiencia laboral
class ExperienciaLaboralForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'id': 'id_fecha_inicio'  # Asegúrate de que el id coincida
        }),
        label="Fecha de Inicio"
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'id': 'id_fecha_fin'  # Asegúrate de que el id coincida
        }),
        label="Fecha de Fin"
    )

    class Meta:
        model = ExperienciaLaboral
        fields = ['empresa', 'cargo', 'fecha_inicio', 'fecha_fin', 'descripcion']

# Formulario para la educación
class EducacionForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'id': 'id_fecha_inicio_educacion'  # Asegúrate de que el id coincida
        }),
        label="Fecha de Inicio"
    )
    fecha_finalizacion = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'id': 'id_fecha_finalizacion'  # Asegúrate de que el id coincida
        }),
        label="Fecha de Finalización"
    )

    class Meta:
        model = Educacion
        fields = ['institucion', 'titulo', 'fecha_inicio', 'fecha_finalizacion']

# Formulario para las habilidades
class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ['nombre_habilidad', 'nivel_competencia']

# Formulario para las referencias
class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Referencia
        fields = ['nombre', 'edad', 'telefono', 'parentesco']

  