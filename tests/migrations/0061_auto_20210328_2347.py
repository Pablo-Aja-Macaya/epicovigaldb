# Generated by Django 3.1.3 on 2021-03-28 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0060_auto_20210328_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineagesmostcommoncountries',
            name='id_process',
        ),
        migrations.RemoveField(
            model_name='lineagestest',
            name='id_process',
        ),
        migrations.RemoveField(
            model_name='nextcladetest',
            name='id_process',
        ),
        migrations.RemoveField(
            model_name='ngsstatstest',
            name='id_process',
        ),
        migrations.RemoveField(
            model_name='singlechecktest',
            name='id_process',
        ),
        migrations.RemoveField(
            model_name='variantstest',
            name='id_process',
        ),
    ]
