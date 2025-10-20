from django.contrib import admin
from . import models  # Importe seu modelo Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'serie_number')

    # Você também pode adicionar outros campos aqui se quiser
    list_display = ('title',)


admin.site.register(models.Product, ProductAdmin)
