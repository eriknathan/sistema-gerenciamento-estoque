from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Configuração do Admin para o modelo Supplier.
    Adiciona a funcionalidade de busca, essencial para o autocomplete_fields.
    """
    list_display = ('name', 'cnpj', 'email', 'phone')
    search_fields = ('name', 'cnpj')
