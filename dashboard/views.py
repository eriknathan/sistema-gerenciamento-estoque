from django.views.generic import TemplateView
from django.db.models import Sum, F
from products.models import Product
from inflows.models import Inflow
from outflows.models import Outflow
from itertools import chain


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()

        # Product Metrics
        context['total_products_count'] = products.count()
        context['low_stock_products_count'] = products.filter(quantity__lt=5).count()

        # Financial Metrics
        stock_value = products.aggregate(
            total_value=Sum(F('quantity') * F('selling_price')),
            total_cost=Sum(F('quantity') * F('cost_price'))
        )
        context['total_stock_value'] = stock_value['total_value'] or 0
        context['total_stock_cost'] = stock_value['total_cost'] or 0
        profit = context['total_stock_value'] - context['total_stock_cost']
        context['total_profit_margin'] = profit

        # Movement Metrics
        sales = Outflow.objects.filter(outflow_type='SALE').annotate(
            total_sale=F('quantity') * F('product__selling_price')
        ).aggregate(
            total_sales_value=Sum('total_sale')
        )
        context['total_sales_value'] = sales['total_sales_value'] or 0

        purchases = Inflow.objects.annotate(
            total_cost=F('quantity') * F('product__cost_price')
        ).aggregate(
            total_purchase_cost=Sum('total_cost')
        )
        context['total_purchase_cost'] = purchases['total_purchase_cost'] or 0

        # Recent Movements
        recent_inflows = list(Inflow.objects.select_related(
            'product').order_by('-created_at')[:5])
        recent_outflows = list(Outflow.objects.select_related(
            'product').order_by('-created_at')[:5])

        for inflow in recent_inflows:
            inflow.movement_type = 'Entrada'
            inflow.total_value = inflow.quantity * inflow.product.cost_price

        for outflow in recent_outflows:
            outflow.movement_type = f"Saída ({outflow.get_outflow_type_display()})"
            val = outflow.quantity * outflow.product.selling_price
            outflow.total_value = val

        recent_movements = sorted(
            chain(recent_inflows, recent_outflows),
            key=lambda x: x.created_at,
            reverse=True
        )[:6]

        context['recent_movements'] = recent_movements

        return context
