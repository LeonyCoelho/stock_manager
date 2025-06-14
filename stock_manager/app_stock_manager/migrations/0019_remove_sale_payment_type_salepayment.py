# Generated by Django 5.2.1 on 2025-06-03 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_stock_manager', '0018_alter_supplier_cnpj'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='payment_type',
        ),
        migrations.CreateModel(
            name='SalePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('DH', 'Dinheiro'), ('PX', 'PIX'), ('DB', 'Débito'), ('CR', 'Crédito'), ('BO', 'Boleto')], max_length=2)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit_installments', models.IntegerField(blank=True, default=1, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app_stock_manager.sale')),
            ],
        ),
    ]
