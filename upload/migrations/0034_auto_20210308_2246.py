# Generated by Django 3.1.3 on 2021-03-08 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0033_auto_20210308_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='samplemetadata',
            old_name='fecha_entrada_uv',
            new_name='fecha_entrada',
        ),
    ]
