# Generated by Django 2.1.2 on 2019-01-02 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contentsInfo',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('contents_id', models.IntegerField()),
                ('uploadfilename', models.CharField(max_length=100)),
                ('ftpsavefilename', models.CharField(max_length=100)),
                ('contentspath', models.CharField(max_length=200)),
                ('hash', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='forum',
            fields=[
                ('contents_id', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('writer', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('tags', models.CharField(blank=True, max_length=50, null=True)),
                ('contents', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='imagesForForum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('path', models.CharField(blank=True, max_length=200, null=True)),
                ('filename', models.CharField(blank=True, max_length=200, null=True)),
                ('contents_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.forum')),
            ],
        ),
        migrations.CreateModel(
            name='myPageInfomation',
            fields=[
                ('apiprovider', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('userimage', models.CharField(blank=True, max_length=200, null=True)),
                ('profile', models.CharField(blank=True, max_length=200, null=True)),
                ('joiningdate', models.DateTimeField(null=True)),
                ('votingcount', models.IntegerField(blank=True, null=True)),
                ('pwd', models.CharField(blank=True, max_length=20, null=True)),
                ('account', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='replyForContents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('writer', models.CharField(blank=True, max_length=50, null=True)),
                ('contents', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='replyForForum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('writer', models.CharField(blank=True, max_length=50, null=True)),
                ('contents', models.CharField(blank=True, max_length=1000, null=True)),
                ('contents_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.forum')),
            ],
        ),
        migrations.CreateModel(
            name='uploadContents',
            fields=[
                ('contents_id', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('writeremail', models.CharField(max_length=50)),
                ('filename', models.CharField(max_length=100)),
                ('contentspath', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=50)),
                ('publisheddate', models.DateTimeField()),
                ('category', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('tags', models.CharField(max_length=50)),
                ('fileinfo', models.CharField(max_length=250)),
                ('totalpages', models.IntegerField()),
                ('previewpath', models.CharField(max_length=250)),
                ('authorinfo', models.CharField(max_length=1000)),
                ('intro', models.CharField(max_length=1000)),
                ('index', models.CharField(max_length=1000)),
                ('contents', models.CharField(max_length=1000)),
                ('reference', models.CharField(default=True, max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='voters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('list_of_voters', models.CharField(blank=True, max_length=50, null=True)),
                ('contents_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.forum')),
            ],
        ),
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.CharField(blank=True, max_length=100, null=True)),
                ('privateKey', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.IntegerField(blank=True, null=True)),
                ('transactions', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.AddField(
            model_name='replyforcontents',
            name='writeremail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.uploadContents'),
        ),
    ]
