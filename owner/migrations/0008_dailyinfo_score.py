# Generated by Django 5.0.2 on 2024-07-18 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0007_remove_dailyinfo_is_firsttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyinfo',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
