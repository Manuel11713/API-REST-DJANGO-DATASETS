# Generated by Django 3.1.3 on 2020-11-06 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201105_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='row',
            old_name='dataset_id',
            new_name='dataset',
        ),
    ]
