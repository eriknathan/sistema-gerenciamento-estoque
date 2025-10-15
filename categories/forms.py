from django import forms
from . import models


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }
