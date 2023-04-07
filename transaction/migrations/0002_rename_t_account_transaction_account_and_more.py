# Generated by Django 4.2 on 2023-04-07 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='t_account',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='t_customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='t_loan',
            new_name='loan',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='t_teller',
            new_name='teller',
        ),
    ]
