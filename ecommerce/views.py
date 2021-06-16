from django.views import generic
from django.shortcuts import render
from .models import Product

class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 4

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_details.html'
