# Generated by Django 3.1.3 on 2021-04-19 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0077_auto_20210418_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantstest',
            name='alt',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='alt_aa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='alt_codon',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref_aa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref_codon',
            field=models.CharField(max_length=100),
        ),
    ]