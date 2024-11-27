from django.urls import path
from app_stock_manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('customers/new/', views.new_customer, name='new_customer'),
    path('customers/', views.view_customers, name='view_customers'),
    path('suppliers/new/', views.new_supplier, name='new_supplier'),
    path('suppliers/', views.view_suppliers, name='view_suppliers'),
    path('products/new/', views.new_product, name='new_product'),
    path('products/', views.view_products, name='view_products'),
    path('stocks/', views.view_stocks, name='view_stocks'),
    # ========== POST API =====================================================
    path('add-customer/', views.add_customer, name='add_customer'),
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('add-product/', views.add_product, name='add_product'),
    # ========== GET API =====================================================
    path('api/categories/', views.get_all_categories, name='get_all_categories'),
    path('api/customers/', views.get_all_customers, name='get_all_customers'),
    path('api/suppliers/', views.get_all_suppliers, name='get_all_suppliers'),
    path('api/products/', views.get_all_products, name='get_all_products'),
    path('api/unit-types/', views.get_unit_types, name='get_unit_types'),
    path('api/stocks/', views.get_all_stocks, name='get_all_stocks'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)