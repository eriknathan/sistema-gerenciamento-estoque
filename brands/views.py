from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
from . import models
from . import forms


class BrandListView(ListView):
    model = models.Brand
    template_name = 'brands/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BrandCreateView(CreateView):
    model = models.Brand
    template_name = 'brands/brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')


class BrandDetailView(DetailView):
    model = models.Brand
    template_name = 'brands/brand_detail.html'
    context_object_name = 'brand'


class BrandUpdateView(UpdateView):
    model = models.Brand
    template_name = 'brands/brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')


class BrandDeleteView(DeleteView):
    model = models.Brand
    template_name = 'brands/brand_delete.html'
    success_url = reverse_lazy('brand_list')


def brand_export_csv(request):
    """
    Export list of brands to CSV format.
    Applies the same filtering logic as BrandListView.
    """
    queryset = models.Brand.objects.all()
    name = request.GET.get('name')

    if name:
        queryset = queryset.filter(name__icontains=name)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename="marcas.csv"'}
    )
    # Add UTF-8 BOM so Excel opens it correctly directly
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Descrição', 'Status', 'Criado em'])

    for brand in queryset:
        status = 'Ativo' if brand.is_active else 'Inativo'
        created_at = brand.created_at.strftime('%d/%m/%Y %H:%M') \
            if brand.created_at else ''
        writer.writerow([
            brand.id,
            brand.name,
            brand.description or '',
            status,
            created_at
        ])

    return response
