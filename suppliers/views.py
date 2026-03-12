from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
from . import models
from . import forms


class SupplierListView(ListView):
    model = models.Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class SupplierCreateView(CreateView):
    model = models.Supplier
    template_name = 'suppliers/supplier_create.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')


class SupplierDetailView(DetailView):
    model = models.Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'


class SupplierUpdateView(UpdateView):
    model = models.Supplier
    template_name = 'suppliers/supplier_update.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')


class SupplierDeleteView(DeleteView):
    model = models.Supplier
    template_name = 'suppliers/supplier_delete.html'
    success_url = reverse_lazy('supplier_list')


def supplier_export_csv(request):
    """
    Export list of suppliers to CSV format.
    Applies the same filtering logic as SupplierListView.
    """
    queryset = models.Supplier.objects.all()
    name = request.GET.get('name')

    if name:
        queryset = queryset.filter(name__icontains=name)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8',
        headers={'Content-Disposition':
                 'attachment; filename="fornecedores.csv"'}
    )
    # Add UTF-8 BOM so Excel opens it correctly directly
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'CNPJ', 'Telefone', 'Email', 'Endereço',
                     'Criado em'])

    for supplier in queryset:
        created_at = supplier.created_at.strftime('%d/%m/%Y %H:%M') \
            if supplier.created_at else ''
        writer.writerow([
            supplier.id,
            supplier.name,
            supplier.cnpj or '',
            supplier.phone or '',
            supplier.email or '',
            supplier.address or '',
            created_at
        ])

    return response
