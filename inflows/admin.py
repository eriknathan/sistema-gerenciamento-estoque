from django.contrib import admin
from . import models


class InflowAdmin(admin.ModelAdmin):
    """
    Configuração personalizada para o modelo Inflow no Django Admin.
    """

    # 1. Colunas que aparecem na lista (baseado no seu, mas adicionei 'user')
    list_display = (
        'product',
        'quantity',
        'supplier',
        'user',
        'created_at',
        'invoice_number',
    )

    # 2. Campos que a barra de busca irá consultar
    #    (Corrigido de 'supplier_name' para 'supplier__name')
    search_fields = (
        'product__title',  # Busca dentro do título do produto
        'supplier__name',  # Busca dentro do nome do fornecedor
        'invoice_number',
        'user__username'   # Permite buscar pelo nome do usuário
    )

    # 3. Filtros que aparecem na barra lateral direita (NOVO)
    list_filter = (
        'supplier',
        'product',
        'user',
        'created_at',
    )

    # 4. Campos que são apenas para leitura no formulário (NOVO)
    readonly_fields = ('created_at', 'updated_at')

    # 5. Otimização para Chaves Estrangeiras (FK) (NOVO)
    #    Substitui <select> por um campo de busca, muito mais rápido.
    autocomplete_fields = ('product', 'supplier', 'user')

    # 6. Organização do formulário de criação/edição (NOVO)
    fieldsets = (
        ('Informações Principais', {
            'fields': ('product', 'supplier', 'quantity')
        }),
        ('Detalhes da Transação', {
            'fields': ('invoice_number', 'user', 'description')
        }),
        ('Datas (Automático)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Esconde esta seção por padrão
        }),
    )


admin.site.register(models.Inflow, InflowAdmin)
