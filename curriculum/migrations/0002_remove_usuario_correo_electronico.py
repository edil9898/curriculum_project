# Generated by Django 5.1.2 on 2024-10-24 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='correo_electronico',
        ),
    ]
