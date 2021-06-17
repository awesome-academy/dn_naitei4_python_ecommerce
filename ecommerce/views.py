from django.views import generic
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product

class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 4

class ProductDetailView(generic.DetailView):
    model = Product

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
