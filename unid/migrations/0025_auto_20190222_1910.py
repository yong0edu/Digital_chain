# Generated by Django 2.1.2 on 2019-02-22 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0024_contentsnouns'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fundpost',
            old_name='ddd',
            new_name='fundaccount',
        ),
        migrations.RenameField(
            model_name='fundpost',
            old_name='eee',
            new_name='txid',
        ),
    ]
