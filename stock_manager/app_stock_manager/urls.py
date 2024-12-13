from django.urls import path
from app_stock_manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='login'),
    path("logout/", views.user_logout, name="logout"),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('settings/', views.settings, name='settings'),
    path('customers/new/', views.new_customer, name='new_customer'),
    path('customers/', views.view_customers, name='view_customers'),
    path('suppliers/new/', views.new_supplier, name='new_supplier'),
    path('suppliers/', views.view_suppliers, name='view_suppliers'),
    path('products/new/', views.new_product, name='new_product'),
    path('products/', views.view_products, name='view_products'),
    path('stocks/', views.view_stocks, name='view_stocks'),
    path('sales/', views.view_sales, name='view_sales'),
    path('sales/new/', views.new_sale, name='new_sale'),
    path('purchases/', views.view_purchases, name='view_purchases'),
    path('purchases/new/', views.new_purchase, name='new_purchase'),
    # ========== POST API =====================================================
    path('add-customer/', views.add_customer, name='add_customer'),
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path("api/stocks/<int:stock_id>/update/", views.update_stock, name="update_stock"),
    path('api/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('api/boletos/<int:boleto_id>/pay/', views.pay_boleto, name='pay_boleto'),


    path("relatorios/produtos/", views.gerar_relatorio_produtos, name="relatorio_produtos"),
    path('relatorios/compras/', views.gerar_relatorio_compras, name='relatorio_compras'),
    path('relatorios/vendas/', views.gerar_relatorio_vendas, name='relatorio_vendas'),

    # ========== GET API =====================================================
    path('api/categories/', views.get_all_categories, name='get_all_categories'),
    path('api/customers/', views.get_all_customers, name='get_all_customers'),
    path('api/suppliers/', views.get_all_suppliers, name='get_all_suppliers'),
    path('api/products/', views.get_all_products, name='get_all_products'),
    path('api/products/search/', views.api_products, name='api_products'),
    path('api/unit-types/', views.get_unit_types, name='get_unit_types'),
    path('api/stocks/', views.get_all_stocks, name='get_all_stocks'),
    path('api/sales/', views.get_all_sales, name='get_all_sales'),
    path('api/purchases/', views.get_all_purchases, name='get_all_purchases'),
    path('api/summary/', views.get_summary, name='api_summary'),
    path('api/sales/latest/', views.get_latest_sales, name='api_latest_sales'),
    path('api/purchases/latest/', views.get_latest_purchases, name='api_latest_purchases'),
    path('api/boletos-pendentes/', views.get_boletos_pendentes, name='boletos_pendentes'),
    path('api/negative-stocks/', views.get_negative_stocks, name='get_negative_stocks'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)