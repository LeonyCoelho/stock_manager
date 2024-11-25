from django.urls import path
from app_stock_manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/new/', views.new_customer, name='new_customer'),
    path('customers/', views.view_customers, name='view_customers'),
    # ========== FUNCIONS =====================================================
    path('add-customer/', views.add_customer, name='add_customer'),
    # ========== API =====================================================
    path('api/customers/', views.get_all_customers, name='get_all_customers'),
    path('api/products/', views.get_all_products, name='get_all_products'),
    path('api/stock/', views.get_stock, name='get_stock'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)