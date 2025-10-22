from django import forms
from . import models


class InflowForm(forms.ModelForm):

    class Meta:
        model = models.Inflow

        fields = [
            'product',
            'supplier',
            'quantity',
            'invoice_number',
            'description',
        ]

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 100'
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº da nota fiscal (Opcional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alguma observação sobre a entrada? (Opcional)'
            }),
        }

        labels = {
            'product': 'Produto',
            'supplier': 'Fornecedor',
            'quantity': 'Quantidade',
            'invoice_number': 'Nota Fiscal',
            'description': 'Descrição',
        }
