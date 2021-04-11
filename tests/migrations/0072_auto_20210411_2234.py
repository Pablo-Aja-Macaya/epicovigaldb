# Generated by Django 3.1.3 on 2021-04-11 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0071_auto_20210405_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextcladetest',
            name='clade',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='nextcladetest',
            name='qc_missing_data_status',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='nextcladetest',
            name='qc_mixed_sites_status',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='nextcladetest',
            name='qc_private_mutations_status',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='nextcladetest',
            name='qc_snp_clusters_status',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
    ]
