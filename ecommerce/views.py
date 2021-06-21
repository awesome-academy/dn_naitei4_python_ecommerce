from django.urls.base import reverse
from ecommerce.forms import ProfileForm, UserForm
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Product

class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 8

class ProductDetailView(generic.DetailView):
    model = Product

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('user-page')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'ecommerce/profile.html', {'user_form': user_form,'profile_form': profile_form})
