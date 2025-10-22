from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from . import models
from . import forms


class OutflowListView(LoginRequiredMixin, ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
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


class OutflowCreateView(LoginRequiredMixin, CreateView):
    model = models.Outflow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflows_list')

    def form_valid(self, form):
        """
        Este método é chamado quando o formulário é validado com sucesso.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class OutflowDetailView(LoginRequiredMixin, DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflow'
