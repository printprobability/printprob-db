# Generated by Django 3.0.4 on 2020-09-26 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pp', '0036_auto_20200925_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='x_max',
            field=models.IntegerField(help_text='X-axis index for the end of this character on the page image'),
        ),
        migrations.AlterField(
            model_name='character',
            name='x_min',
            field=models.IntegerField(help_text='X-axis index for the start of this character on the page image'),
        ),
        migrations.AlterField(
            model_name='character',
            name='y_max',
            field=models.IntegerField(help_text='Y-axis index for the end of this character on the page image', null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='y_min',
            field=models.IntegerField(help_text='Y-axis index for the start of this character on the page image', null=True),
        ),
    ]
