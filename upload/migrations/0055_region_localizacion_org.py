# Generated by Django 3.1.3 on 2021-05-29 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0054_auto_20210529_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='localizacion_org',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
