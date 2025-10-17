import re
from django import forms
from . import models


class SupplierForm(forms.ModelForm):

    def clean_cnpj(self):
        """Remove a máscara do CNPJ e valida o formato."""
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove caracteres não numéricos
            cnpj = re.sub(r'[^0-9]', '', cnpj)

            # Valida se o CNPJ tem 14 dígitos
            if len(cnpj) != 14:
                raise forms.ValidationError(
                    'O CNPJ deve conter 14 dígitos.'
                )
        return cnpj

    class Meta:
        model = models.Supplier
        fields = ['name', 'cnpj', 'email', 'phone', 'address', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contato@empresa.com.br'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3}),
        }
        labels = {
            'name': 'Nome',
            'cnpj': 'CNPJ',
            'email': 'E-mail',
            'phone': 'Telefone',
            'address': 'Endereço',
            'description': 'Descrição',
        }
