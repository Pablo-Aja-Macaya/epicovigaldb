# Generated by Django 3.1.3 on 2021-04-10 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0040_auto_20210405_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='pais',
            field=models.CharField(default='SPAIN', max_length=50),
        ),
        migrations.AlterField(
            model_name='region',
            name='region',
            field=models.CharField(default='EUROPE', max_length=50),
        ),
    ]
