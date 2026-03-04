from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from . import models
from . import forms


class OutflowListView(ListView):
    model = models.Outflow
    template_name = 'outflows/outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(
                Q(product__title__icontains=search_term) |
                Q(invoice_number__icontains=search_term)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.db.models import Sum, F
        outflows = models.Outflow.objects.all()
        
        context['outflows_count'] = outflows.count()
        context['quantity_sold'] = outflows.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        # Calcular valor total das vendas e lucro
        # Somente saídas do tipo SALE devem contar para valor e lucro
        sales = outflows.filter(outflow_type=models.Outflow.OutflowType.SALE)
        
        context['total_sales'] = sales.aggregate(
            total_value=Sum(F('quantity') * F('product__selling_price'))
        )['total_value'] or 0

        total_cost = sales.aggregate(
            total_cost=Sum(F('quantity') * F('product__cost_price'))
        )['total_cost'] or 0

        context['total_profit'] = context['total_sales'] - total_cost

        return context



class OutflowCreateView(CreateView):
    model = models.Outflow
    template_name = 'outflows/outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflows_list')


class OutflowDetailView(DetailView):
    model = models.Outflow
    template_name = 'outflows/outflow_detail.html'
    context_object_name = 'outflow'
