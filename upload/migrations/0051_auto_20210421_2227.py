# Generated by Django 3.1.3 on 2021-04-21 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0050_auto_20210419_0042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='samplemetadata',
            old_name='ct_redrp',
            new_name='ct_rdrp',
        ),
    ]
