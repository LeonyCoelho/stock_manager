from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Customer, Product, Stock, Supplier, Category, Sale, SaleProduct, Purchase, PurchaseProduct, Boleto
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, Count, Min
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required



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

def view_sales(request):
    return render(request, 'pages/list_sales.html')

def new_sale(request):
    return render(request, 'pages/new_sale.html')

def view_purchases(request):
    return render(request, 'pages/list_purchases.html')

def new_purchase(request):
    return render(request, 'pages/new_purchase.html')



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
    
@login_required
@csrf_exempt
def add_sale(request):
    if request.method == "POST":
        try:
            # Verificar se o usuário está autenticado (para APIs que não usam sessões, pode ser via token)
            if not request.user.is_authenticated:
                return JsonResponse({"success": False, "error": "Usuário não autenticado"}, status=401)

            # Carregar os dados do corpo da requisição
            data = json.loads(request.body)
            customer_id = data.get("customer")

            # Valida se o cliente existe
            customer = get_object_or_404(Customer, id=customer_id)

            # Inicializa variáveis
            sale_name = data.get("name", "")
            observations = data.get("observations", "")
            payment_type = data.get("payment_type", "")
            products = data.get("products", [])

            # Calcula o preço total
            total_price = Decimal(0.00)  # Inicializa como Decimal
            for product_data in products:
                product = get_object_or_404(Product, id=product_data["id"])

                # Verifica se o produto tem estoque e pega o preço
                stock = product.stocks.first()
                if not stock:
                    return JsonResponse({"success": False, "error": f"Produto {product.name} sem estoque."}, status=400)
                
                stock_price = Decimal(stock.price)  # Converte para Decimal
                quantity = Decimal(product_data["quantity"])  # Converte para Decimal
                total_price += stock_price * quantity  # Atualiza o preço total com Decimal

            # Verifica se campos obrigatórios estão presentes
            required_fields = ["name", "customer", "payment_type", "products"]
            missing_fields = [field for field in required_fields if field not in data or not data[field]]

            if missing_fields:
                return JsonResponse(
                    {"success": False, "error": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"},
                    status=400,
                )

            # Criação da venda
            sale = Sale.objects.create(
                user=request.user,  # Associa o usuário logado à venda
                name=sale_name,
                customer=customer,
                observations=observations,
                payment_type=payment_type,
                full_price=total_price,  # Salva o preço total como Decimal
            )

            # Adicionar produtos à venda
            for product_data in products:
                product = get_object_or_404(Product, id=product_data["id"])
                stock = product.stocks.first()
                if not stock:
                    continue  # Se o produto não tem estoque, não adiciona

                stock_price = Decimal(stock.price)  # Converte para Decimal
                quantity = Decimal(product_data["quantity"])  # Converte para Decimal

                SaleProduct.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    price=stock_price,  # Salva o preço unitário
                )

            # Adicionar boletos (se aplicável)
            if payment_type == "BO":
                print("Boleto")
                installments = data.get("installments", [])
                for installment in installments:
                    installment_value = Decimal(installment["value"])  # Converte para Decimal
                    Boleto.objects.create(
                        sale=sale,
                        value=installment_value,
                        due_date=installment["due_date"],
                        status="Pendente",
                    )

            return JsonResponse({"success": True, "sale_id": sale.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Método não permitido"}, status=405)



@csrf_exempt
def add_purchase(request):
    if request.method == "POST":
        try:
            # Parse os dados JSON enviados
            data = json.loads(request.body)

            # Captura e valida o fornecedor (supplier)
            supplier_id = data.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplier_id)

            # Captura o usuário (ajuste conforme sua lógica de autenticação)
            user = request.user

            # Inicializa o valor total da compra
            full_price = Decimal(0.00)

            # Cria a compra dentro de uma transação
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    user=user,
                    name=data.get("name"),
                    supplier=supplier,
                    observations=data.get("observations", ""),
                    full_price=full_price  # Atualizaremos depois de calcular o preço total
                )

                # Processa os produtos
                products = data.get("products", [])
                for item in products:
                    product = get_object_or_404(Product, id=item.get("id"))
                    quantity = Decimal(item.get("quantity", 1))

                    # Verifica o preço do produto no estoque
                    stock, created = Stock.objects.get_or_create(product=product)

                    # Atualiza o estoque (incrementa a quantidade)
                    stock.quantity += quantity
                    stock.save()

                    # Calcula o total do item
                    item_total = stock.price * quantity
                    full_price += item_total

                    # Cria o PurchaseProduct
                    PurchaseProduct.objects.create(
                        purchase=purchase,
                        product=product,
                        quantity=quantity,
                        price=stock.price
                    )

                # Atualiza o preço total da compra
                purchase.full_price = full_price
                purchase.save()

            # Retorna resposta de sucesso
            return JsonResponse({"success": True, "message": "Compra registrada com sucesso!"}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método não permitido."}, status=405)

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
            # Atualiza o preço 
            new_price = data.get("price")
            if new_price is not None:
                stock.price = new_price
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

def api_products(request):
    query = request.GET.get('search', '')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    # Adicionando o menor preço do estoque relacionado
    products_with_price = products.annotate(min_price=Min('stocks__price'))

    data = {
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "weight": product.weight,
                "unit_type": product.unit_type,
                "size": product.size,
                "quantity_per_package": product.quantity_per_package,
                "price": product.min_price if product.min_price is not None else 0  # Garantindo que o preço não seja nulo
            }
            for product in products_with_price
        ]
    }
    return JsonResponse(data)

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

def get_all_sales(request):
    sales = Sale.objects.all()
    sale_list = []

    for sale in sales:
        sale_products = [
            {
                "product_id": sale_product.product.id,
                "product_name": sale_product.product.name,
                "quantity": float(sale_product.quantity),
                "price": float(sale_product.price),
                "total_price": float(sale_product.quantity * sale_product.price),
            }
            for sale_product in sale.sale_products.all()
        ]

        sale_list.append({
            "sale_id": sale.id,
            "sale_name": sale.name,
            "sale_created": sale.created,
            "customer_name": sale.customer.name,
            "full_price": float(sale.full_price),
            "products": sale_products,
        })

    return JsonResponse({"sales": sale_list})

def get_all_purchases(request):
    purchases = Purchase.objects.all()
    purchase_list = []

    for purchase in purchases:
        purchase_products = [
            {
                "product_id": purchase_product.product.id,
                "product_name": purchase_product.product.name,
                "quantity": float(purchase_product.quantity),
                "price": float(purchase_product.price),
                "total_price": float(purchase_product.quantity * purchase_product.price),
            }
            for purchase_product in purchase.purchase_products.all()
        ]

        purchase_list.append({
            "purchase_id": purchase.id,
            "purchase_name": purchase.name,
            "purchase_created": purchase.created,
            "supplier_name": purchase.supplier.name,
            "full_price": float(purchase.full_price),
            "products": purchase_products,
        })

    return JsonResponse({"purchases": purchase_list})

def get_summary(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Filtros para vendas e compras
    daily_sales = Sale.objects.filter(created__date=today)
    daily_purchases = Purchase.objects.filter(created__date=today)
    weekly_sales = Sale.objects.filter(created__date__gte=start_of_week)
    weekly_purchases = Purchase.objects.filter(created__date__gte=start_of_week)
    monthly_sales = Sale.objects.filter(created__date__gte=start_of_month)
    monthly_purchases = Purchase.objects.filter(created__date__gte=start_of_month)

    # Função auxiliar para calcular resumo
    def calculate_summary(sales, purchases):
        sales_products = SaleProduct.objects.filter(sale__in=sales)
        purchases_products = PurchaseProduct.objects.filter(purchase__in=purchases)

        return {
            'sales_total': sales.aggregate(total=Sum('full_price'))['total'] or 0,
            'products_sold': sales_products.aggregate(total=Sum('quantity'))['total'] or 0,
            'purchases_total': purchases.aggregate(total=Sum('full_price'))['total'] or 0,
            'products_purchased': purchases_products.aggregate(total=Sum('quantity'))['total'] or 0,
        }

    # Resumo diário, semanal e mensal
    data = {
        'daily': calculate_summary(daily_sales, daily_purchases),
        'weekly': calculate_summary(weekly_sales, weekly_purchases),
        'monthly': calculate_summary(monthly_sales, monthly_purchases),
    }

    return JsonResponse(data)

def get_latest_sales(request):
    sales = Sale.objects.order_by('-created')[:10]
    data = {
        'sales': [
            {
                'sale_name': sale.name,
                'customer_name': sale.customer.name,
                'sale_created': sale.created,
                'full_price': sale.full_price,
            }
            for sale in sales
        ]
    }
    return JsonResponse(data)

def get_latest_purchases(request):
    purchases = Purchase.objects.order_by('-created')[:10]
    data = {
        'purchases': [
            {
                'purchase_name': purchase.name,
                'supplier_name': purchase.supplier.name,
                'purchase_created': purchase.created,
                'full_price': purchase.full_price,
            }
            for purchase in purchases
        ]
    }
    return JsonResponse(data)

