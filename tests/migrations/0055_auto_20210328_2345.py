# Generated by Django 3.1.3 on 2021-03-28 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0038_auto_20210314_2317'),
        ('tests', '0054_auto_20210328_2345'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='singlechecktest',
            unique_together={('id_uvigo', 'id_process', 'date')},
        ),
    ]
