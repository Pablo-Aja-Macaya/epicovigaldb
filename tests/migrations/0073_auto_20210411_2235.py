# Generated by Django 3.1.3 on 2021-04-11 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0072_auto_20210411_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextcladetest',
            name='total_missing',
            field=models.IntegerField(default=None, null=True),
        ),
    ]