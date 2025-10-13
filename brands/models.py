from django.db import models


class Brand(models.Model):
    """Representa uma marca de produto no sistema."""
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True)
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

    def __str__(self):
        """Retorna a representação em string do objeto, que é o nome da marca."""
        return self.name
