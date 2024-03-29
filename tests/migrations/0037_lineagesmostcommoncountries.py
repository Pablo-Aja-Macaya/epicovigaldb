# Generated by Django 3.1.3 on 2021-03-03 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0036_delete_lineagesmostcommoncountries'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineagesMostCommonCountries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_process', models.CharField(max_length=40)),
                ('date', models.DateTimeField(auto_now=True)),
                ('country', models.TextField(blank=True, default=None, max_length=50)),
                ('id_uvigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.lineagestest')),
            ],
        ),
    ]
