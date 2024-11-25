from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer, Product, Stock

def home(request):
    return render(request, 'pages/home.html')

def new_customer(request):
    return render(request, 'pages/new_customer.html')

def view_customers(request):
    return render(request, 'pages/customers.html')
# ======================= FUNCIONS ============================================

def add_customer(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        cep = request.POST.get("cep", "").strip()
        street = request.POST.get("street", "").strip()
        address_number = request.POST.get("address_number", "").strip()
        district = request.POST.get("district", "").strip()
        state = request.POST.get("state", "").strip()
        city = request.POST.get("city", "").strip()
        cpf_or_cnpj = request.POST.get("cpf_or_cnpj", "").strip()
        is_cnpj = request.POST.get("is_cnpj", "").lower() == "true"
        observacoes = request.POST.get("observacoes", "").strip()

        if not name:
            return JsonResponse({"error": "O campo 'Nome' é obrigatório."}, status=400)

        try:
            customer = Customer.objects.create(
                name=name,
                cpf_or_cnpj=cpf_or_cnpj,
                is_cnpj=is_cnpj,
                street=street,
                address_number=address_number,
                district=district,
                city=city,
                state=state,
                cep=cep,
                # Adicione o campo observações no modelo
            )
            return JsonResponse({"message": "Cliente adicionado com sucesso!", "id": customer.id})
        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar cliente: {str(e)}"}, status=500)
    else:
        return redirect('home')

# ======================= API =================================================

def get_all_customers(request):
    customers = Customer.objects.all()
    customer_list = [{
        'id': customer.id,
        'name': customer.name,
        'cpf_or_cnpj': customer.cpf_or_cnpj,
        'is_cnpj': customer.is_cnpj,
        'street': customer.street,
        'address_number': customer.address_number,
        'district': customer.district,
        'city': customer.city,
        'state': customer.state,
        'cep': customer.cep,
    } for customer in customers]

    return JsonResponse({'customers': customer_list})

def get_all_products(request):
    products = Product.objects.all()
    product_list = [{
        'id': product.id,
        'name': product.name,
        'category': product.category,
        'unity_type': product.unity_type,
    } for product in products]

    return JsonResponse({'products': product_list})

def get_stock(request):
    stock_items = Stock.objects.select_related('product').all()
    stock_list = [{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
        },
        'quantity': item.quantity,
        'price': item.price,
        'pending': item.pending,
    } for item in stock_items]

    return JsonResponse({'stock': stock_list})