# Generated by Django 3.1.3 on 2020-12-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PicardTests',
            fields=[
                ('id_test', models.AutoField(primary_key=True, serialize=False)),
                ('id_process', models.IntegerField()),
                ('mean_target_coverage', models.DecimalField(decimal_places=6, max_digits=15)),
                ('median_target_coverage', models.DecimalField(decimal_places=6, max_digits=15)),
                ('pct_target_bases_1x', models.DecimalField(decimal_places=6, max_digits=7)),
                ('pct_target_bases_10x', models.DecimalField(decimal_places=6, max_digits=7)),
                ('pct_target_bases_100x', models.DecimalField(decimal_places=6, max_digits=7)),
            ],
        ),
    ]
