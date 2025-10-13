from django.db import models


class Supplier(models.Model):
    """Representa um fornecedor de produtos."""
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True)
    phone = models.CharField("Telefone", max_length=20, blank=True)
    email = models.EmailField("E-mail", max_length=255, blank=True)
    address = models.TextField("Endereço", blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True, null=True,
                            blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']

    def __str__(self):
        """Retorna a representação em string do objeto, que é o nome do
        fornecedor."""
        return self.name
