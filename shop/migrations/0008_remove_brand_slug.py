# Generated by Django 4.2.6 on 2024-02-22 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_team_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='slug',
        ),
    ]
