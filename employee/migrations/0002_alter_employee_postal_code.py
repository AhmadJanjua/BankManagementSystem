# Generated by Django 4.2 on 2023-04-08 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='postal_code',
            field=models.CharField(max_length=7),
        ),
    ]
