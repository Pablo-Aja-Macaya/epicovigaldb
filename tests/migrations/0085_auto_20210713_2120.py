# Generated by Django 3.1.3 on 2021-07-13 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0084_auto_20210627_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='nextcladetest',
            name='qc_frameshifts_frameshifts',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='nextcladetest',
            name='qc_frameshifts_status',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='nextcladetest',
            name='qc_stopcodons_status',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='nextcladetest',
            name='qc_stopcodons_stopcodons',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]