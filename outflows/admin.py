from django.contrib import admin
from . import models  # Importe seu modelo Product


class OutflowAdmin(admin.ModelAdmin):
    search_fields = ('product', 'quantity')

    # Você também pode adicionar outros campos aqui se quiser
    list_display = ('product',)


admin.site.register(models.Outflow, OutflowAdmin)
