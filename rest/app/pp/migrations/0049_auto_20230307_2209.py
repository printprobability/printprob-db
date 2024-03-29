# Generated by Django 3.2.18 on 2023-03-08 03:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pp', '0048_charactermatch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charactermatch',
            name='match',
        ),
        migrations.AddField(
            model_name='charactermatch',
            name='matches',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.UUIDField(help_text='Matched characters corresponding to a character query'),
                blank=True, default=list, size=20),
        ),
    ]
