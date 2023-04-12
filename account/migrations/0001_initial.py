# Generated by Django 4.2 on 2023-04-12 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_num', models.AutoField(primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Chequing',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='account.account')),
                ('monthly_fee', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            bases=('account.account',),
        ),
        migrations.CreateModel(
            name='Savings',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='account.account')),
                ('interest_rate', models.DecimalField(decimal_places=6, max_digits=12)),
            ],
            bases=('account.account',),
        ),
    ]
