# Generated by Django 3.1.3 on 2021-03-08 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0034_auto_20210308_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplemetadata',
            name='categoria_muestra',
            field=models.CharField(blank=True, default=None, max_length=20),
        ),
    ]
