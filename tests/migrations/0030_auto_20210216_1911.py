# Generated by Django 3.1.3 on 2021-02-16 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0029_delete_variantstest'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantsTest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_uvigo', models.CharField(max_length=20)),
                ('id_process', models.CharField(max_length=41)),
                ('row', models.IntegerField()),
                ('pos', models.IntegerField()),
                ('ref', models.CharField(max_length=10)),
                ('alt', models.CharField(max_length=10)),
                ('alt_freq', models.DecimalField(decimal_places=6, max_digits=7)),
                ('ref_codon', models.CharField(max_length=10)),
                ('ref_aa', models.CharField(max_length=10)),
                ('alt_codon', models.CharField(max_length=10)),
                ('alt_aa', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='variantstest',
            constraint=models.UniqueConstraint(fields=('id_uvigo', 'row', 'id_process'), name='unique_constraint'),
        ),
    ]
