# Generated by Django 5.1 on 2024-10-20 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
