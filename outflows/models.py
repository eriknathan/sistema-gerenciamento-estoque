from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Outflow(models.Model):
    class OutflowType(models.TextChoices):
        SALE = 'SALE', 'Venda'
        LOSS = 'LOSS', 'Perda / Dano'
        ADJUSTMENT = 'ADJUSTMENT', 'Ajuste de Estoque'

    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name="outflows",
                                verbose_name="Produto")
    quantity = models.IntegerField("Quantidade")
    description = models.TextField("Descrição", null=True, blank=True)
    invoice_number = models.CharField("Nota Fiscal", max_length=50, blank=True)
    outflow_type = models.CharField(
        "Tipo de Saída",
        max_length=20,
        choices=OutflowType.choices,
        default=OutflowType.SALE
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             verbose_name="Usuário")
    created_at = models.DateTimeField("Data da Entrada", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'
        ordering = ['-created_at']

    def __str__(self):
        """Retorna uma descrição da transação de entrada."""
        return f"Saída de {str(self.quantity)}x {str(self.product.title)} \
            ({self.get_outflow_type_display()})"
