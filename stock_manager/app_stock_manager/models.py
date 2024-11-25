from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Customer(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    cpf_or_cnpj = models.CharField(max_length=20, verbose_name="CPF ou CNPJ")
    is_cnpj = models.BooleanField(default=False)
    address_number = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    cep = models.CharField(max_length=20)
    observations = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    cpf_or_cnpj = models.CharField(max_length=20, verbose_name="CPF ou CNPJ")
    is_cnpj = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    unity_type = models.CharField(max_length=50, verbose_name="Unit Type")

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    full_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id} - {self.name}"


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sale_products")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchases")
    invoice_number = models.CharField(max_length=50)
    full_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase {self.id} - {self.name}"


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_products")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"