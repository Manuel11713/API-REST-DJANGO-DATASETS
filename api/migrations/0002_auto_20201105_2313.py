# Generated by Django 3.1.3 on 2020-11-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='row',
            old_name='dataset',
            new_name='dataset_id',
        ),
        migrations.AddField(
            model_name='row',
            name='client_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='row',
            name='client_name',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
    ]
