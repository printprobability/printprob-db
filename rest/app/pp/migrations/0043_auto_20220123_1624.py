# Generated by Django 3.2.8 on 2022-01-23 21:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pp', '0042_auto_20210515_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='BreakageType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, default='', editable=False, max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='character',
            name='breakage_types',
            field=models.ManyToManyField(help_text='Types of breakage exhibited by this character.', related_name='characters', to='pp.BreakageType'),
        ),
    ]