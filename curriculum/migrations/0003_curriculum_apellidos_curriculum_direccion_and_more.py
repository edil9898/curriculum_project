# Generated by Django 5.1.2 on 2024-11-03 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_remove_usuario_correo_electronico'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='apellidos',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='nombres',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
