from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Customer, Product, Stock, Supplier, Category
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'pages/home.html')

def settings(request):
    return render(request, 'pages/settings.html')

def view_customers(request):
    return render(request, 'pages/list_customers.html')

def new_customer(request):
    return render(request, 'pages/new_customer.html')

def view_suppliers(request):
    return render(request, 'pages/list_suppliers.html')

def new_supplier(request):
    return render(request, 'pages/new_supplier.html')

def view_products(request):
    return render(request, 'pages/list_products.html')

def new_product(request):
    return render(request, 'pages/new_product.html')

def view_stocks(request):
    return render(request, 'pages/list_stock.html')

# ======================= FUNCIONS ============================================
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            return JsonResponse({"error": "O campo 'Nome' é obrigatório."}, status=400)

        try:
            category = Categories.objects.create(
                name=name,
            )
            return JsonResponse({"message": "Categoria adicionado com sucesso!", "id": category.id})
        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar categoria: {str(e)}"}, status=500)
    else:
        return redirect('home')

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
        observations = request.POST.get("observations", "").strip()

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
                observations=observations,
            )
            return JsonResponse({"message": "Cliente adicionado com sucesso!", "id": customer.id})
        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar cliente: {str(e)}"}, status=500)
    else:
        return redirect('home')

def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        cnpj = request.POST.get("cnpj", "").strip()
        observations = request.POST.get("observations", "").strip()

        if not name:
            return JsonResponse({"error": "O campo 'Nome' é obrigatório."}, status=400)

        try:
            supplier = Supplier.objects.create(
                name=name,
                cnpj=cnpj,
                observations=observations,
            )
            return JsonResponse({"message": "Fornecedor adicionado com sucesso!", "id": supplier.id})
        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar fornecedor: {str(e)}"}, status=500)
    else:
        return redirect('home')

@csrf_exempt
def add_product(request):
    if request.method == "POST":
        try:
            # Tente carregar os dados enviados na requisição
            data = json.loads(request.body)

            # Captura os campos
            name = data.get("name", "").strip()
            weight = data.get("weight", "").strip()
            unit_type = data.get("unit_type", "").strip()
            size = data.get("size", "").strip()
            quantity_per_package = data.get("quantity_per_package", "").strip()
            observations = data.get("observations", "").strip()

            # Validações
            if not name:
                return JsonResponse({"error": "O campo 'Nome' é obrigatório."}, status=400)
            if not weight.isdigit() or int(weight) <= 0:
                return JsonResponse({"error": "O campo 'Gramas' deve ser um número positivo."}, status=400)
            if not size or "x" not in size:
                return JsonResponse({"error": "O campo 'Formato' deve ser no formato 'NxM'."}, status=400)
            if not quantity_per_package.isdigit() or int(quantity_per_package) <= 0:
                return JsonResponse({"error": "O campo 'Quantidade por Pacote' deve ser um número positivo."}, status=400)

            # Salva o produto no banco de dados
            product = Product.objects.create(
                name=name,
                weight=int(weight),
                unit_type=unit_type,
                size=size,
                quantity_per_package=int(quantity_per_package),
                observations=observations,
            )

            # Cria o perfil no estoque com quantidade inicial 0
            Stock.objects.create(
                product=product,
                quantity=0,  # Quantidade inicial
                price=0.0,   # Preço inicial, ajuste se necessário
            )
            return JsonResponse({"message": "Produto adicionado com sucesso!", "id": product.id})
        except json.JSONDecodeError as e:
            # Erro ao decodificar JSON
            return JsonResponse({"error": f"Dados JSON inválidos: {str(e)}"}, status=400)
        except Exception as e:
            # Outros erros
            return JsonResponse({"error": f"Erro ao processar a solicitação: {str(e)}"}, status=500)

    # Se o método não for POST
    return JsonResponse({"error": "Método não permitido."}, status=405)
    
@csrf_exempt
def update_stock(request, stock_id):
    if request.method == "POST":
        try:
            stock = get_object_or_404(Stock, id=stock_id)
            data = json.loads(request.body)

            # Atualiza a quantidade
            new_quantity = data.get("quantity")
            if new_quantity is not None:
                stock.quantity = new_quantity
                stock.save()

            return JsonResponse({"success": True, "message": "Estoque atualizado com sucesso."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método não permitido."}, status=405)

@csrf_exempt
def delete_product(request, product_id):
    """
    View para deletar um produto pelo ID.
    Aceita apenas requisições DELETE.
    """
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return JsonResponse({"message": "Produto deletado com sucesso."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método não permitido."}, status=405)
# ======================= API =================================================

def get_all_categories(request):
    categories = Category.objects.all()
    categories_list = [{
        "id": category.id,
        'name': category.name
    } for category in categories]

    return JsonResponse({'categories': categories_list})

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
        'observations': customer.observations,
    } for customer in customers]

    return JsonResponse({'customers': customer_list})

def get_all_suppliers(request):
    suppliers = Supplier.objects.all()
    supplier_list = [{
        'id': supplier.id,
        'name': supplier.name,
        'cnpj': supplier.cnpj,
        'observations': supplier.observations,
    } for supplier in suppliers]

    return JsonResponse({'suppliers': supplier_list})

def get_all_products(request):
    products = Product.objects.all()
    product_list = [{
        'id': product.id,
        'name': product.name,
        'weight': product.weight,
        'unit_type': product.get_unit_type_display(),
        'size': product.size,
        # 'category': product.category.name,
        'quantity_per_package': product.quantity_per_package,
    } for product in products]

    return JsonResponse({'products': product_list})

def get_unit_types(request):
    unit_types = [{"value": key, "label": value} for key, value in dict(Product.UNIT_CHOICES).items()]
    return JsonResponse({"unit_types": unit_types})

def get_all_stocks(request):
    stock_items = Stock.objects.select_related('product').all()
    stock_list = [{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'weight': item.product.weight,  # Gramatura do produto
            'size': item.product.size,  # Formato do produto (ex.: "66x96")
            'quantity_per_package': item.product.quantity_per_package,  # Quantidade por pack
            # 'category': item.product.category.name,
        },
        'quantity': item.quantity,
        'price': item.price,
        'pending': item.pending,
    } for item in stock_items]

    return JsonResponse({'stock': stock_list})