from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from datetime import datetime
from django.urls import reverse_lazy
from .filters import ProductFilter
from .forms import ProductForm


class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class ProductsDetail(DetailView):
    model = Product
    ordering = 'name'
    template_name = 'product.html'
    context_object_name = 'product'


class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductUpdate(UpdateView):
    from_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
    fields = '__all__'


class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
