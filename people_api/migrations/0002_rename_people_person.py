# Generated by Django 4.1 on 2023-02-11 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='People',
            new_name='Person',
        ),
    ]
