# Generated by Django 5.0.2 on 2024-03-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_userhealth_healthproblemcontent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
