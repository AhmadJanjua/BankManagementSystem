# Generated by Django 4.2 on 2023-04-09 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loan', '0001_initial'),
        ('customer', '0001_initial'),
        ('account', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_num', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.account')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.customer')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loan.loan')),
                ('teller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.teller')),
            ],
        ),
    ]
