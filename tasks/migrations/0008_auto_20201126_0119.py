# Generated by Django 3.1.3 on 2020-11-26 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20201126_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='longitude',
            field=models.TextField(default='NULL', max_length=50),
        ),
    ]
