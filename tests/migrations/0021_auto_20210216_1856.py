# Generated by Django 3.1.3 on 2021-02-16 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_auto_20210216_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantstest',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='id_uvigo',
            field=models.CharField(max_length=20),
        ),
    ]
