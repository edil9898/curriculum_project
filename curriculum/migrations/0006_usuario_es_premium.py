# Generated by Django 5.1.2 on 2024-11-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0005_remove_usuario_foto_curriculum_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='es_premium',
            field=models.BooleanField(default=False),
        ),
    ]
