# Generated by Django 2.1.2 on 2019-02-07 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0002_auto_20190202_0007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadcontents',
            old_name='ccc',
            new_name='cagegory_path',
        ),
    ]
