# Generated by Django 3.1.3 on 2021-02-16 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_auto_20210213_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantstest',
            name='row',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]