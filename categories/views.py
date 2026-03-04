from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
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
