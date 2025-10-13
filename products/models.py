from django.db import models
from categories.models import Category
from brands.models import Brand


class Product(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT,
                                 related_name='products')
    description = models.TextField("Descrição", null=True, blank=True)
    serie_number = models.CharField("SKU / Número de Série", max_length=200,
                                    null=True, blank=True)
    cost_price = models.DecimalField("Preço de Custo", max_digits=20,
                                     decimal_places=2)
    selling_price = models.DecimalField("Preço de Venda", max_digits=20,
                                        decimal_places=2)
    quantity = models.IntegerField("Quantidade em Estoque", default=0)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.title
