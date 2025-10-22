from django import forms
from . import models


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product

        fields = [
            'title',
            'category',
            'brand',
            'description',
            'serie_number',
            'quantity',
            'cost_price',
            'selling_price',
        ]
        
        labels = {
            'title': 'Título do Produto',
            'category': 'Categoria',
            'brand': 'Marca',
            'description': 'Descrição',
            'serie_number': 'Número de Série / SKU',
            'quantity': 'Quantidade em Estoque',
            'cost_price': 'Preço de Custo (R$)',
            'selling_price': 'Preço de Venda (R$)',
        }

        help_texts = {
            'serie_number': 'O SKU, código de barras ou outro identificador único.',
            'quantity': 'A quantidade inicial deste produto.',
            'cost_price': 'O valor que você pagou pelo produto.',
            'selling_price': 'O valor que o cliente final pagará.',
        }

        # 3. Widgets otimizados
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Teclado Gamer XYZ'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select' 
            }),
            'brand': forms.Select(attrs={
                'class': 'form-select',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 100',
                'min': '0'  # Boa prática para estoque
            }),
            'description': forms.Textarea(attrs={ 
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalhes, especificações, cor, etc.'
            }),
            'serie_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 12345-ABC'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150.00',
                'step': '0.01'
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 299.90',
                'step': '0.01'
            }),
        }

        # 4. Mensagens de erro personalizadas (Opcional)
        error_messages = {
            'title': {
                'required': 'O título do produto é obrigatório.',
                'unique': 'Já existe um produto com este título.'
            },
            'selling_price': {
                'required': 'O preço de venda é obrigatório.'
            },
        }

    # 5. Validação customizada (Melhoria Avançada)
    def clean(self):
        """
        Adiciona validações customizadas entre múltiplos campos.
        """
        cleaned_data = super().clean()
        cost_price = cleaned_data.get("cost_price")
        selling_price = cleaned_data.get("selling_price")

        # Garante que o preço de venda não é menor que o de custo
        if cost_price is not None and selling_price is not None:
            if selling_price < cost_price:
                # Adiciona um erro específico ao campo 'selling_price'
                self.add_error('selling_price', 'O preço de venda não pode ser menor que o preço de custo.')

        return cleaned_data
