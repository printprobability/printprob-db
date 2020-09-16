# Generated by Django 3.0.4 on 2020-06-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pp', '0025_auto_20200603_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='tif_md5',
        ),
        migrations.RemoveField(
            model_name='spread',
            name='tif_md5',
        ),
        migrations.AddField(
            model_name='characterrun',
            name='script_version',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='linerun',
            name='script_version',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='pagerun',
            name='script_version',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]