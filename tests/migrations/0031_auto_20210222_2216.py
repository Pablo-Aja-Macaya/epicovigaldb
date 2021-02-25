# Generated by Django 3.1.3 on 2021-02-22 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0030_auto_20210216_1911'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='variantstest',
            name='unique_constraint',
        ),
        migrations.AddConstraint(
            model_name='variantstest',
            constraint=models.UniqueConstraint(fields=('id_uvigo', 'row', 'id_process', 'date'), name='unique_constraint'),
        ),
    ]