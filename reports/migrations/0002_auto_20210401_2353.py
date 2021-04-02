# Generated by Django 3.1.3 on 2021-04-01 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monthly_Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicial', models.DateField(blank=True, null=True)),
                ('fecha_final', models.DateField(blank=True, null=True)),
                ('variantes', models.TextField(default=None, max_length=50)),
                ('subtitulo', models.TextField(default=None, max_length=50)),
                ('texto', models.TextField(blank=True, default=None, max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='fecha_final',
        ),
        migrations.RemoveField(
            model_name='report',
            name='fecha_inicial',
        ),
        migrations.RemoveField(
            model_name='report',
            name='subtitulo',
        ),
        migrations.RemoveField(
            model_name='report',
            name='texto',
        ),
        migrations.RemoveField(
            model_name='report',
            name='variantes',
        ),
        migrations.AlterField(
            model_name='report',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]