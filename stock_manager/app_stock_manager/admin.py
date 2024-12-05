from django.contrib import admin
from .models import (
    Category,
    Customer,
    Supplier,
    Product,
    Stock,
    Sale,
    SaleProduct,
    Purchase,
    PurchaseProduct,
    Boleto,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    ordering = ("id",)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cpf_or_cnpj", "is_cnpj", "city", "state", "created")
    search_fields = ("name", "cpf_or_cnpj", "city", "state")
    list_filter = ("is_cnpj", "state")
    ordering = ("id",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cnpj")
    search_fields = ("name", "cnpj")
    ordering = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit_type")
    search_fields = ("id", "name")
    ordering = ("id",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "price", "pending")
    search_fields = ("product__name",)
    list_filter = ("product",)
    ordering = ("id",)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "customer", "full_price", "created")
    search_fields = ("name", "user__username", "customer__name")
    list_filter = ("created",)
    ordering = ("id",)


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sale", "product", "quantity", "price")
    search_fields = ("sale__name", "product__name")
    ordering = ("id",)

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ("id", "sale", "due_date", "value", "status")

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "supplier", "invoice_number", "full_price", "created")
    search_fields = ("name", "user__username", "supplier__name", "invoice_number")
    list_filter = ("created",)
    ordering = ("id",)


@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase", "product", "quantity", "price")
    search_fields = ("purchase__name", "product__name")
    ordering = ("id",)
