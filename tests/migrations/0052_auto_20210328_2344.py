# Generated by Django 3.1.3 on 2021-03-28 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0038_auto_20210314_2317'),
        ('tests', '0051_remove_picardtest_id_process'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='variantstest',
            name='unique_constraint',
        ),
        migrations.AlterUniqueTogether(
            name='lineagestest',
            unique_together={('id_uvigo', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='nextcladetest',
            unique_together={('id_uvigo', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='ngsstatstest',
            unique_together={('id_uvigo', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='singlechecktest',
            unique_together={('id_uvigo', 'date')},
        ),
        migrations.AddConstraint(
            model_name='variantstest',
            constraint=models.UniqueConstraint(fields=('id_uvigo', 'row', 'date'), name='unique_constraint'),
        ),
    ]
