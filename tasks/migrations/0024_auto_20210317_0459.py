# Generated by Django 3.1.3 on 2021-03-17 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0023_team_team_component'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='image',
            field=models.ImageField(upload_to='static/tasks'),
        ),
    ]
