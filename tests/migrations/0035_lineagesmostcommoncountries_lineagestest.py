# Generated by Django 3.1.3 on 2021-03-03 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0031_auto_20210303_0301'),
        ('tests', '0034_auto_20210303_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineagesMostCommonCountries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_process', models.CharField(max_length=40)),
                ('date', models.DateTimeField(auto_now=True)),
                ('country', models.TextField(blank=True, default=None, max_length=50)),
                ('id_uvigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.sample')),
            ],
        ),
        migrations.CreateModel(
            name='LineagesTest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_process', models.CharField(max_length=40)),
                ('lineage', models.CharField(max_length=10)),
                ('probability', models.DecimalField(decimal_places=6, max_digits=7)),
                ('pangolearn_version', models.CharField(blank=True, max_length=15)),
                ('comments', models.TextField(blank=True, default=None, max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('id_uvigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.sample')),
            ],
            options={
                'unique_together': {('id_uvigo', 'id_process', 'date')},
            },
        ),
    ]