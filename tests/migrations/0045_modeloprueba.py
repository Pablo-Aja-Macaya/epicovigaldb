# Generated by Django 3.1.3 on 2021-03-26 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0044_delete_modeloprueba'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloPrueba',
            fields=[
                ('id_uvigo', models.IntegerField(primary_key=True, serialize=False)),
                ('atr1', models.CharField(max_length=10)),
            ],
        ),
    ]
