# Generated by Django 3.1.3 on 2020-11-30 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20201130_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='id_sample',
            new_name='id_uvigo',
        ),
    ]
