from django.db.models.signals import pre_delete
from django.dispatch import receiver
from app_stock_manager.models import Customer, Sale, Supplier, Purchase, SaleProduct, PurchaseProduct, Product

@receiver(pre_delete, sender=Customer)
def save_customer_name_before_delete(sender, instance, **kwargs):
    """Antes de excluir um cliente, salva o nome nas vendas associadas."""
    Sale.objects.filter(customer=instance).update(customer_name=instance.name)

@receiver(pre_delete, sender=Supplier)
def save_supplier_name_before_delete(sender, instance, **kwargs):
    """Antes de excluir um fornecedor, salva o nome nas compras associadas."""
    Purchase.objects.filter(supplier=instance).update(supplier_name=instance.name)

@receiver(pre_delete, sender=Product)
def save_product_info_before_delete(sender, instance, **kwargs):
    """Antes de excluir um produto, salva o ID e nome nas tabelas dependentes."""
    
    SaleProduct.objects.filter(product=instance).update(product_info=f"{instance.id} - {instance.name}")
    PurchaseProduct.objects.filter(product=instance).update(product_info=f"{instance.id} - {instance.name}")
