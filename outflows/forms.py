from django import forms
from django.core.exceptions import ValidationError
from . import models


class OutflowForm(forms.ModelForm):
    """
    Formulário para o modelo Outflow.
    """
    class Meta:
        model = models.Outflow

        fields = [
            'product',
            'quantity',
            'outflow_type',
            'invoice_number',
            'description',
        ]

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 100',
            }),
            'outflow_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº da nota fiscal (Opcional) - Ex: NF-12345'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alguma observação sobre a entrada? (Opcional)',
            }),
        }

        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'outflow_type': 'Tipo de Saída',
            'invoice_number': 'Nota Fiscal',
            'description': 'Descrição',
        }

    def clean_quantity(self):
        """
        Valida a quantidade de saída.
        """
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        # Garante que ambos os campos existem antes de comparar
        if quantity and product:
            if quantity <= 0:
                raise ValidationError('A quantidade deve ser maior que zero.')
            if quantity > product.quantity:
                raise ValidationError(
                    f'A quantidade de saída ({quantity}) é maior que o estoque disponível ({product.quantity}) para o produto "{product.title}".'
                )

        return quantity
