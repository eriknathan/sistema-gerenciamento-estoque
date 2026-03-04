import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from brands.models import Brand
from categories.models import Category
from suppliers.models import Supplier
from products.models import Product
from inflows.models import Inflow
from outflows.models import Outflow

def create_super_user():
    print("Criando superusuário admin:admin...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

def populate_brands():
    print("Criando marcas...")
    brands_data = ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'Logitech', 'Asus', 'Acer', 'HP', 'Lenovo']
    brands = []
    for name in brands_data:
        brand, _ = Brand.objects.get_or_create(name=name, defaults={'description': f'Marca {name} original'})
        brands.append(brand)
    return brands

def populate_categories():
    print("Criando categorias...")
    categories_data = ['Smartphones', 'Laptops', 'Acessórios', 'Monitores', 'Áudio', 'Televisores']
    categories = []
    for name in categories_data:
        category, _ = Category.objects.get_or_create(name=name, defaults={'description': f'Produtos da categoria {name}'})
        categories.append(category)
    return categories

def populate_suppliers():
    print("Criando fornecedores...")
    suppliers_data = [
        {'name': 'Distribuidora Tech', 'cnpj': '12345678000199', 'phone': '11999999999', 'email': 'tech@dist.com', 'address': 'Rua Tech, 123'},
        {'name': 'Global Eletrônicos', 'cnpj': '98765432000188', 'phone': '11888888888', 'email': 'global@eletronicos.com', 'address': 'Av Global, 456'},
        {'name': 'SupriMundo', 'cnpj': '45612378000177', 'phone': '11777777777', 'email': 'vendas@suprimundo.com', 'address': 'Rua Suprimentos, 789'},
    ]
    suppliers = []
    for data in suppliers_data:
        supplier, _ = Supplier.objects.get_or_create(cnpj=data['cnpj'], defaults=data)
        suppliers.append(supplier)
    return suppliers

def populate_products(brands, categories):
    print("Criando produtos...")
    products_data = [
        {'title': 'iPhone 15 Pro', 'category': categories[0], 'brand': brands[0], 'cost_price': 5000.00, 'selling_price': 7500.00, 'serie_number': 'IP15P-001'},
        {'title': 'Galaxy S24 Ultra', 'category': categories[0], 'brand': brands[1], 'cost_price': 4500.00, 'selling_price': 6500.00, 'serie_number': 'GLX-S24U'},
        {'title': 'Dell XPS 13', 'category': categories[1], 'brand': brands[4], 'cost_price': 6000.00, 'selling_price': 8500.00, 'serie_number': 'DL-XPS13-55'},
        {'title': 'MacBook Pro M3', 'category': categories[1], 'brand': brands[0], 'cost_price': 8000.00, 'selling_price': 12000.00, 'serie_number': 'MBP-M3-99'},
        {'title': 'Monitor LG UltraGear 27', 'category': categories[3], 'brand': brands[3], 'cost_price': 1200.00, 'selling_price': 1800.00, 'serie_number': 'LG-UG27'},
        {'title': 'Headphone Sony WH-1000XM5', 'category': categories[4], 'brand': brands[2], 'cost_price': 1500.00, 'selling_price': 2200.00, 'serie_number': 'SN-WH5'},
        {'title': 'Mouse Logitech MX Master 3S', 'category': categories[2], 'brand': brands[5], 'cost_price': 400.00, 'selling_price': 650.00, 'serie_number': 'MXM3S-00'},
        {'title': 'Smart TV 55 4K', 'category': categories[5], 'brand': brands[1], 'cost_price': 2000.00, 'selling_price': 3000.00, 'serie_number': 'SMTV-55'},
        {'title': 'Asus ROG Zephyrus', 'category': categories[1], 'brand': brands[6], 'cost_price': 9000.00, 'selling_price': 13000.00, 'serie_number': 'ROG-Z14'},
        {'title': 'Teclado Mecânico Keychron', 'category': categories[2], 'brand': brands[5], 'cost_price': 500.00, 'selling_price': 800.00, 'serie_number': 'KCH-K8'},
    ]
    
    products = []
    for data in products_data:
        product, _ = Product.objects.get_or_create(serie_number=data['serie_number'], defaults={
            'title': data['title'],
            'category': data['category'],
            'brand': data['brand'],
            'cost_price': data['cost_price'],
            'selling_price': data['selling_price'],
            'quantity': 0, # Estoque começa zerado
            'description': f"Produto {data['title']} de alta qualidade."
        })
        products.append(product)
    return products

def populate_movements(products, suppliers):
    print("Criando entradas e saídas e ajustando estoque...")
    admin_user = User.objects.filter(username='admin').first()
    
    # 1. Entradas (Inflows)
    for product in products:
        # Fazer 1 a 3 entradas para cada produto
        for i in range(random.randint(1, 3)):
            quantity = random.randint(10, 50)
            Inflow.objects.create(
                product=product,
                supplier=random.choice(suppliers),
                quantity=quantity,
                invoice_number=f"NF-{random.randint(1000, 9999)}",
                user=admin_user,
                description="Entrada de estoque inicial"
            )
            # Atualizar estoque
            product.quantity += quantity
            product.save()

    # 2. Saídas (Outflows)
    for product in products:
        # Apenas dar saída se houver algo no estoque
        if product.quantity > 5:
            # Fazer 1 a 5 vendas/saídas
            for i in range(random.randint(1, 5)):
                quantity = random.randint(1, min(5, product.quantity))
                outflow_type = random.choice([Outflow.OutflowType.SALE, Outflow.OutflowType.SALE, Outflow.OutflowType.SALE, Outflow.OutflowType.LOSS]) # Mais propensão a venda
                Outflow.objects.create(
                    product=product,
                    quantity=quantity,
                    outflow_type=outflow_type,
                    invoice_number=f"NF-S-{random.randint(1000, 9999)}",
                    user=admin_user,
                    description=f"Saída tipo: {outflow_type}"
                )
                # O Signal no Outflow normalmente já deve atualizar o estoque se configurado,
                # mas se não tiver signal, atualizamos manualmente. Modelos SGE podem usar Signals.
                # Para evitar duplicidade, checamos se precisamos manual.
                # Assumindo atualização manual para garantir:
                # product.quantity -= quantity
                # product.save()

    print("Movimentações criadas!")

def run():
    print("=== Iniciando População do Banco de Dados ===")
    create_super_user()
    brands = populate_brands()
    categories = populate_categories()
    suppliers = populate_suppliers()
    products = populate_products(brands, categories)
    populate_movements(products, suppliers)
    print("=== Banco de dados populado com sucesso! ===")

if __name__ == '__main__':
    run()
