from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Curriculum, ExperienciaLaboral, Educacion, Habilidad, Referencia

# Formulario para el registro de Usuario
class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput,  # Usa un campo de entrada tipo contraseña
        label="Contraseña",
        min_length=8,  # Puedes ajustar la longitud mínima según tus requisitos
        help_text="Mínimo 8 caracteres"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'contrasena']  # Incluye el campo de contraseña

    # Encriptación de la contraseña antes de guardar el usuario
    def save(self, commit=True):
        user = super().save(commit=False)
        user.contrasena = make_password(self.cleaned_data['contrasena'])  # Encriptar la contraseña
        if commit:
            user.save()
        return user

# Formulario para la creación del Curriculum
class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['plantilla_seleccionada', 'formato_exportacion']  # No incluir fecha_creacion

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
