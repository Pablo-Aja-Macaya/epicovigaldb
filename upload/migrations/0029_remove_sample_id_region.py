# Generated by Django 3.1.3 on 2021-03-02 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0028_auto_20210302_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='id_region',
        ),
    ]
