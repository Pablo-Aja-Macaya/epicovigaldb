# Generated by Django 3.1.3 on 2021-06-17 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0081_auto_20210505_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantstest',
            name='alt_dp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='variantstest',
            name='ref_dp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='variantstest',
            name='total_dp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='alt',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='alt_aa',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='alt_codon',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='pos',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref_aa',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='variantstest',
            name='ref_codon',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]
