# Generated by Django 5.1.1 on 2024-09-20 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_addons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboard',
            name='work_type',
        ),
    ]
