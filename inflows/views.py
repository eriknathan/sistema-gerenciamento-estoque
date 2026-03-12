from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse

from . import models
from . import forms


class InflowListView(ListView):
    model = models.Inflow
    template_name = 'inflows/inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('product')

        if product:
            queryset = queryset.filter(product__title__icontains=product)

        return queryset


class InflowCreateView(CreateView):
    model = models.Inflow
    template_name = 'inflows/inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')


class InflowDetailView(DetailView):
    model = models.Inflow
    template_name = 'inflows/inflow_detail.html'
    context_object_name = 'inflows'


def inflow_export_csv(request):
    """
    Export list of inflows to CSV format.
    Applies the same filtering logic as InflowListView.
    """
    queryset = models.Inflow.objects.all()
    product = request.GET.get('product')

    if product:
        queryset = queryset.filter(product__title__icontains=product)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename="entradas.csv"'}
    )
    # Add UTF-8 BOM so Excel opens it correctly directly
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Produto', 'Qtd.', 'Fornecedor', 'Nota Fiscal',
                     'Usuário', 'Data'])

    for inflow in queryset:
        created_at = inflow.created_at.strftime('%d/%m/%Y %H:%M') \
            if inflow.created_at else ''
        writer.writerow([
            inflow.id,
            inflow.product.title if inflow.product else '',
            inflow.quantity,
            inflow.supplier.name if inflow.supplier else '',
            inflow.invoice_number or '',
            inflow.user.username if inflow.user else '',
            created_at
        ])

    return response
