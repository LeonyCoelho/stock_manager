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
    path('settings/new_user', views.new_user, name='new_user'),
    path('customers/new/', views.new_customer, name='new_customer'),
    path("customer/edit/<int:customer_id>/", views.edit_customer, name="edit_customer"),
    path("customer/delete/<int:customer_id>/", views.delete_customer, name="delete_customer"),

    path('customers/', views.view_customers, name='view_customers'),
    path('suppliers/new/', views.new_supplier, name='new_supplier'),
    path('suppliers/', views.view_suppliers, name='view_suppliers'),
    path("supplier/edit/<int:supplier_id>/", views.edit_supplier, name="edit_supplier"),
    path("supplier/delete/<int:supplier_id>/", views.delete_supplier, name="delete_supplier"),

    path('products/new/', views.new_product, name='new_product'),
    path('products/', views.view_products, name='view_products'),
    path('stocks/', views.view_stocks, name='view_stocks'),
    path('sales/', views.view_sales, name='view_sales'),
    path('sales/new/', views.new_sale, name='new_sale'),
    path("sale/delete/<int:sale_id>/", views.delete_sale, name="delete_sale"),
    path("api/quotes/<int:sale_id>/convert/", views.convert_quote_to_sale, name="convert_quote_to_sale"),  # Converter orçamento em venda
    path('purchases/', views.view_purchases, name='view_purchases'),
    path('purchases/new/', views.new_purchase, name='new_purchase'),
    path("purchase/delete/<int:purchase_id>/", views.delete_purchase, name="delete_purchase"),
    path("quote/edit/<int:quote_id>/", views.edit_quote, name="edit_quote"),
    path("quote/edit/<int:quote_id>/", views.edit_quote, name="edit_quote"),
    path("quote/update/<int:quote_id>/", views.update_quote, name="update_quote"),


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
    path('api/quotes/', views.get_all_quotes, name='get_all_quotes'),
    path('api/categories/', views.get_all_categories, name='get_all_categories'),
    path('api/customers/', views.get_all_customers, name='get_all_customers'),
    path('api/suppliers/', views.get_all_suppliers, name='get_all_suppliers'),
    path('api/products/', views.get_all_products, name='get_all_products'),
    path('api/products/search/', views.api_products, name='api_products'),
    path('api/products/<int:product_id>/prices/', views.get_product_prices, name='product-prices'),
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