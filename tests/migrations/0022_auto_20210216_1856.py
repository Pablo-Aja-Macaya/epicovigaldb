# Generated by Django 3.1.3 on 2021-02-16 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0021_auto_20210216_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantstest',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
