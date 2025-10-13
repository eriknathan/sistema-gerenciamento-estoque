from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from suppliers.models import Supplier


class Inflow(models.Model):
    """Representa uma entrada de produto no estoque."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="inflows", verbose_name="Produto")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,
                                 verbose_name="Fornecedor",
                                 related_name="inflows")
    quantity = models.IntegerField("Quantidade")
    invoice_number = models.CharField("Nota Fiscal", max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             verbose_name="Usuário")
    description = models.TextField("Descrição", null=True, blank=True)
    created_at = models.DateTimeField("Data da Entrada", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['-created_at']

    def __str__(self):
        """Retorna uma descrição da transação de entrada."""
        return f"Entrada de {str(self.quantity)}x {str(self.product.title)}"
