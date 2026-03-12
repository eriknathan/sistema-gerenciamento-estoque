from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
from . import models
from . import forms


class CategoryListView(ListView):
    model = models.Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categorys'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CategoryCreateView(CreateView):
    model = models.Category
    template_name = 'categories/category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDetailView(DetailView):
    model = models.Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'


class CategoryUpdateView(UpdateView):
    model = models.Category
    template_name = 'categories/category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = models.Category
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('category_list')


def category_export_csv(request):
    """
    Export list of categories to CSV format.
    Applies the same filtering logic as CategoryListView.
    """
    queryset = models.Category.objects.all()
    name = request.GET.get('name')

    if name:
        queryset = queryset.filter(name__icontains=name)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8',
        headers={'Content-Disposition':
                 'attachment; filename="categorias.csv"'}
    )
    # Add UTF-8 BOM so Excel opens it correctly directly
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Descrição', 'Status', 'Criado em'])

    for category in queryset:
        status = 'Ativo' if category.is_active else 'Inativo'
        created_at = category.created_at.strftime('%d/%m/%Y %H:%M') \
            if category.created_at else ''
        writer.writerow([
            category.id,
            category.name,
            category.description or '',
            status,
            created_at
        ])

    return response
