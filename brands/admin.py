from django.contrib import admin
from . import models


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at',
                    'updated_at')
    search_fields = ('name',)


admin.site.register(models.Brand, BrandAdmin)
