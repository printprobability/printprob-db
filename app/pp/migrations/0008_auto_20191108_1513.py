# Generated by Django 2.2.6 on 2019-11-08 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pp', '0007_auto_20191108_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characterrun',
            name='params',
        ),
        migrations.RemoveField(
            model_name='characterrun',
            name='script_md5',
        ),
        migrations.RemoveField(
            model_name='characterrun',
            name='script_path',
        ),
        migrations.RemoveField(
            model_name='linegrouprun',
            name='params',
        ),
        migrations.RemoveField(
            model_name='linegrouprun',
            name='script_md5',
        ),
        migrations.RemoveField(
            model_name='linegrouprun',
            name='script_path',
        ),
        migrations.RemoveField(
            model_name='linerun',
            name='params',
        ),
        migrations.RemoveField(
            model_name='linerun',
            name='script_md5',
        ),
        migrations.RemoveField(
            model_name='linerun',
            name='script_path',
        ),
        migrations.RemoveField(
            model_name='pagerun',
            name='params',
        ),
        migrations.RemoveField(
            model_name='pagerun',
            name='script_md5',
        ),
        migrations.RemoveField(
            model_name='pagerun',
            name='script_path',
        ),
    ]