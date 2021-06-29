from my_app.settings import EMAIL_HOST_USER
from ecommerce.forms import ProfileForm, UserForm
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from .models import Booking, Cart, Category, Order, Product

def product_get(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'product_list':products,
        'category_list':categories
    }
    return render(request, 'ecommerce/product_list.html',context=context)

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

@login_required
@transaction.atomic
def cart_add(request, pk):
    if request.method == 'POST':
        quantity = request.POST['quantity']
    else:
        quantity = 0

    product_get = Product.objects.filter(pk=pk).first()
    if product_get:
        product_stock = product_get.quantity
    else:
        product_stock = 0

    in_cart = Cart.objects.filter(user=request.user, product__pk=pk).first()
    if in_cart:
        cart_quantity = in_cart.quantity
    else:
        cart_quantity = 0
    
    if int(quantity) > 0 :
        if int(quantity) + cart_quantity > product_stock:
            messages.add_message(request, messages.INFO, _("Out of stock limit"))
        else:
            if in_cart:
                in_cart.quantity = int(quantity) + cart_quantity
                in_cart.save()
            else:
                product_new = Cart(user=request.user, product=Product.objects.get(pk=pk), quantity=quantity)
                product_new.save()
            messages.add_message(request, messages.INFO, _('You added a product to your cart'))
    else:
        messages.add_message(request, messages.INFO, _('Please add product quantity more than 0'))
    
    return redirect(f'/ecommerce/product/{pk}')

@login_required
def cart_get(request):
    cart = Cart.objects.filter(user=request.user).select_related('product')
    stock_changed = False
    total_price = 0
    for item in cart:
        in_stock = item.product.quantity
        if in_stock == 0:
            Cart.objects.filter(user=request.user, product=item.product).delete()
            stock_changed = True
        elif item.quantity > in_stock:
            messages.add_message(request, messages.INFO, _(f"{item.product.product_name} is out of stock limit, please decrease your product items"))
            stock_changed = True
        total_price += item.product.price * item.quantity

    return render(request, 'ecommerce/cart.html', {'cart': cart, 'changed':stock_changed, 'total':total_price})

@login_required
def increase_product_in_cart(request, pk):
    product_get = Product.objects.filter(pk=pk).first()
    if product_get:
        product_stock = product_get.quantity
    else:
        product_stock = 0

    item = Cart.objects.filter(user=request.user, product__pk=pk).first()
    if item:
        cart_quantity = item.quantity
    else:
        cart_quantity = 0
    
    if cart_quantity + 1 > product_stock:
        messages.add_message(request, messages.INFO, _("Out of stock limit"))
    else:
        item.quantity = cart_quantity + 1
        item.save()
        messages.add_message(request, messages.INFO, _('You added one more item of product to your cart'))
    
    return redirect('/ecommerce/cart/')

@login_required
def decrease_product_in_cart(request, pk):
    item = Cart.objects.filter(user=request.user, product__pk=pk).first()
    if item:
        cart_quantity = item.quantity
    else:
        cart_quantity = 0

    if cart_quantity > 0:
        item.quantity = cart_quantity - 1
        if item.quantity == 0 :
            item.delete()
            messages.add_message(request, messages.INFO, _('You deleted product out of your cart'))
        else: 
            item.save()
            messages.add_message(request, messages.INFO, _('You deleted one item of product out of your cart'))
    else:
        raise ValueError(_('Cart quantity must be more than 0'))
    
    return redirect('/ecommerce/cart/')

@login_required
def remove_from_cart(request, pk):
    Cart.objects.filter(user=request.user, product__pk=pk).delete()
    messages.add_message(request, messages.INFO, _('Product has been removed from cart'))
    return redirect('/ecommerce/cart/')

@login_required
@transaction.atomic
def cart_checkout(request):
    cart = Cart.objects.filter(user=request.user).select_related('product')
    total_price = 0

    for item in cart:
        item_quantity = item.quantity
        product_stock = item.product.quantity

        if product_stock == 0:
            item.delete()
            total_price += item.product.price * item.quantity
        elif item_quantity > product_stock:
            messages.add_message(request, messages.INFO, _(f"{item.product.product_name} is out of stock limit, please decrease your product items in your cart"))
            return redirect('/ecommerce/cart')
        else:
            total_price += item.product.price * item.quantity

    if request.method == 'POST':
        shipping_address = request.POST['shipping_address']
        phone_number = request.POST['phone_number']
    else:
        shipping_address = ''
        phone_number = ''

    if shipping_address and phone_number:
        order = Order(user=request.user, shipping_address=shipping_address, phone_number=phone_number, total_price=total_price, status='W')

        if order:
            order.save()
            messages.add_message(request, messages.INFO, _('Order is waiting for being approved by admin! Please wait the approve message!'))
            send_mail(f'New order #{order.id} status annoucement',f'New order #{order.id} have been made, please check waiting order.', EMAIL_HOST_USER , [EMAIL_HOST_USER] ,fail_silently=False,)
            # Xử lý giảm số hàng của sản phẩm trong kho sau khi order
            for item in cart:
                order_detail = Booking(order=order, quantity=item.quantity, product=Product.objects.get(id=item.product.pk))
                order_detail.save()
                item.product.quantity -= item.quantity
                item.product.save()
            # Xử lý làm rỗng giỏ hàng
            Cart.objects.filter(user=request.user).delete()
            return redirect('/ecommerce/')
        else:
            messages.add_message(request, messages.INFO, _('Order is invalid, try again!'))
    else:
        messages.add_message(request, messages.INFO, _('Shipping address or phone number is invalid!'))

    return render(request, 'ecommerce/checkout.html', {'cart': cart, 'total': total_price})

@login_required
def order_get(request):
    orders_list = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'ecommerce/order.html', {'order': orders_list})

@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    detail = Booking.objects.filter(order=pk).select_related('product')

    return render(request, 'ecommerce/order_detail.html', {'id': pk, 'status': order.status, 'detail': detail, 'total': order.total_price})

class OrderAllListView(PermissionRequiredMixin, generic.ListView):
    model = Order
    permission_required = 'ecommerce.can_mark_returned'
    template_name = 'ecommerce/order_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.order_by('-date')

@login_required
@permission_required('ecommerce.can_mark_returned', raise_exception=True)
def check_order_status(request, pk):
    if request.method == 'POST':
        status = request.POST['status']
    else:
        status = 'W'
    
    order = Order.objects.filter(id=pk).first()
    order.status = status
    order.save()

    if status == 'A':
        send_mail(f'Your order #{pk} status annoucement',f'Your order #{pk} have been accepted, please wait for delivery. Big thanks for your support.', EMAIL_HOST_USER , [order.user.username],fail_silently=False,)
    elif  status == 'R':
        send_mail(f'Your order #{pk} status annoucement',f'Your order #{pk} have been rejected, please check your order in our page. Big thanks for your support.', EMAIL_HOST_USER , [order.user.username],fail_silently=False,)
    return redirect('/ecommerce/order/all/')

def product_search(request):
    products = Product.objects.all()
    category_object = Category.objects.all()

    if 'product_name' in request.GET:
        product_name = request.GET["product_name"]
        products = products.filter(product_name__icontains=product_name)

    if 'filter' in request.GET:
        category_name = request.GET["filter"]
        if category_name != 'All':
            products = products.filter(category__name=category_name)

    if 'minimum' and 'maximum' in request.GET:
        minimum = request.GET["minimum"]
        maximum = request.GET["maximum"]
        if minimum and maximum:
            products = products.filter(price__range=[minimum,maximum])
    
    context = {
        'product_list': products, 
        'category_list':category_object
    }

    return render(request, 'ecommerce/product_list.html', context=context)
