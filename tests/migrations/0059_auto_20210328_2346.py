# Generated by Django 3.1.3 on 2021-03-28 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0058_auto_20210328_2346'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='variantstest',
            name='unique_constraint',
        ),
        migrations.AddConstraint(
            model_name='variantstest',
            constraint=models.UniqueConstraint(fields=('id_uvigo', 'row', 'date'), name='unique_constraint'),
        ),
    ]
