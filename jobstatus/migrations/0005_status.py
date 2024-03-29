# Generated by Django 3.1.3 on 2021-06-19 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobstatus', '0004_delete_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id_proceso', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('tarea', models.TextField(max_length=50)),
                ('status', models.CharField(choices=[('O', 'En curso'), ('C', 'Completado'), ('S', 'Almacenado'), ('F', 'Fallido')], max_length=20)),
                ('comentario', models.TextField(max_length=100)),
                ('fecha', models.DateTimeField()),
                ('tiempo', models.IntegerField()),
            ],
        ),
    ]
