from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta
from django.db import models
import random
from app_stock_manager.models import (
    Category, Customer, Supplier, Product, Stock, Sale, SaleProduct, Boleto, Purchase, PurchaseProduct
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com informações fictícias'

    def handle(self, *args, **kwargs):
        # Busca o usuário 'admin'
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Usuário 'admin' não encontrado. Certifique-se de criar o usuário antes de executar este script."))
            return

        # Limpar duplicatas de categorias
        all_categories = Category.objects.values('name').annotate(count=models.Count('id')).filter(count__gt=1)
        for category in all_categories:
            duplicates = Category.objects.filter(name=category['name'])
            # Mantém apenas uma categoria
            duplicates.exclude(id=duplicates.first().id).delete()

        self.stdout.write("Categorias duplicadas foram removidas.")

        # Categorias
        categories = ["Eletrônicos", "Papelaria", "Ferramentas", "Móveis", "Alimentos"]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
        self.stdout.write(f"Categorias criadas: {categories}")

        # Clientes
        for i in range(5):
            Customer.objects.create(
                name=f"Cliente {i+1}",
                cpf_or_cnpj=f"123.456.789-0{i}",
                is_cnpj=False,
                address_number=f"{i+1}",
                street=f"Rua {i+1}",
                district="Bairro Central",
                city="Cidade Exemplo",
                state="Estado",
                cep="12345-678",
            )
        self.stdout.write("Clientes criados.")

        # Fornecedores
        for i in range(3):
            Supplier.objects.create(
                name=f"Fornecedor {i+1}",
                cnpj=f"12.345.678/000{i+1}-00",
            )
        self.stdout.write("Fornecedores criados.")

        # Produtos
        category = Category.objects.first()
        for i in range(10):
            Product.objects.create(
                name=f"Produto {i+1}",
                weight=i * 100,
                category=category,
                unit_type="un",
                size="10x10",
                quantity_per_package="5",
            )
        self.stdout.write("Produtos criados.")

        # Estoque
        for product in Product.objects.all():
            Stock.objects.create(
                product=product,
                quantity=10,
                price=10.00,
                pending=0,
            )
        self.stdout.write("Estoque criado.")

        # Compras
        supplier = Supplier.objects.first()
        for i in range(5):
            purchase = Purchase.objects.create(
                user=user,
                name=f"Compra {i+1}",
                supplier=supplier,
                invoice_number=f"INV{i+1}",
                full_price=500.00,
            )
            for product in Product.objects.all()[:3]:
                PurchaseProduct.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=10,
                    price=10.00,
                )
        self.stdout.write("Compras criadas.")

        customers = Customer.objects.all()
        products = Product.objects.all()
        # Vendas
        for i in range(3):
            sale = Sale.objects.create(
                user=user,
                name=f"Venda {i+1}",
                nfe=f"NFE-{i+1}",
                customer=random.choice(customers),
                full_price=Decimal(random.uniform(500, 3000)),
                payment_type=random.choice(['AV', 'CR', 'BO']),
                observations=f"Observação da venda {i+1}"
            )
            for _ in range(5):
                SaleProduct.objects.create(
                    sale=sale,
                    product=random.choice(products),
                    quantity=Decimal(random.randint(1, 10)),
                    price=Decimal(random.uniform(20, 200))
                )

            # Boletos (apenas para vendas com pagamento em boleto)
            if sale.payment_type == 'BO':
                Boleto.objects.create(
                    sale=sale,
                    value=sale.full_price,
                    due_date=datetime.now() + timedelta(days=random.randint(10, 30)),
                    status=random.choice(["Pendente", "Pago"])
                )
        self.stdout.write("Vendas e boletos criados.")
        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))
