from django.db.models import Sum, F, DecimalField
from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms
from categories.models import Category 
from brands.models import Brand


class ProductListView(ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'Products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Lógica de Filtro
        title = self.request.GET.get('title')
        serie_number = self.request.GET.get('serie_number')
        category_id = self.request.GET.get('category_id')
        brand_id = self.request.GET.get('brand_id')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if serie_number:
            queryset = queryset.filter(serie_number__icontains=serie_number)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pega o queryset filtrado (base da página atual)
        queryset = self.get_queryset()

        # 1. Adiciona as listas para os filtros dropdown
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()

        # 2. Calcula e adiciona as Métricas
        #    (Estou assumindo que você tem um campo 'stock_quantity' no seu model Product)
        metrics = queryset.aggregate(
            total_count=Sum('quantity'),
            total_cost=Sum(F('quantity') * F('cost_price'),
                           output_field=DecimalField()),
            total_value=Sum(F('quantity') * F('selling_price'),
                            output_field=DecimalField())
        )

        total_cost = metrics.get('total_cost') or 0
        total_value = metrics.get('total_value') or 0

        context['total_products_count'] = metrics.get('total_count') or 0
        context['total_stock_cost'] = total_cost
        context['total_stock_value'] = total_value
        context['total_stock_profit'] = total_value - total_cost

        return context


class ProductCreateView(CreateView):
    model = models.Product
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'product_detail.html'
    context_object_name = 'Products'


class ProductUpdateView(UpdateView):
    model = models.Product
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = models.Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
