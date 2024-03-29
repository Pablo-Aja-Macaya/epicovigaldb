# Generated by Django 3.1.3 on 2021-02-28 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_auto_20210228_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id_team', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, default=None, max_length=150)),
                ('descripción', models.TextField(blank=True, default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Team_Component',
            fields=[
                ('id_person', models.AutoField(primary_key=True, serialize=False)),
                ('person', models.CharField(blank=True, default=None, max_length=30)),
                ('id_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.team')),
            ],
        ),
    ]
