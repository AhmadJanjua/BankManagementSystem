# Generated by Django 4.2 on 2023-04-08 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_delete_admin_admin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin',
        ),
    ]