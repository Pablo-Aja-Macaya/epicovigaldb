# Generated by Django 3.1.3 on 2021-02-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0023_auto_20210216_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantstest',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='id_uvigo',
            field=models.CharField(max_length=20),
        ),
    ]