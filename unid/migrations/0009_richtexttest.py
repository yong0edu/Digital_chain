# Generated by Django 2.1.2 on 2019-02-13 17:38

from django.db import migrations, models
import django.db.models.deletion
import social_django.fields


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0008_auto_20190212_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='richtextTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('delta_content', social_django.fields.JSONField(blank=True, default=dict, null=True)),
                ('published', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
    ]
