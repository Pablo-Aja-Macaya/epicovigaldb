# Generated by Django 3.1.3 on 2021-03-02 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0029_remove_sample_id_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='id_region',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
