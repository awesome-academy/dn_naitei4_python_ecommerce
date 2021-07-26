import datetime
from ecommerce.serializers import ProductSerializer
import xlwt
from ecommerce.resources import ProductResource
from tablib import Dataset
from django.db.models.aggregates import Max
from django.http.response import JsonResponse
from my_app.settings import EMAIL_HOST_USER, HOST
from ecommerce.forms import CartForm, CommentForm, ProfileForm, ReviewForm, UserForm
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import date
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.template.loader import render_to_string, get_template
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, pagination
from django.shortcuts import render
from .models import Booking, Cart, Category, Comment, FavoriteProduct, Order, Product, Review

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

class APIProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

def product_get(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        favorite_product_ids = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_product_ids=[]

    context = {
        'category_list':categories,
        'favorite_product_ids':favorite_product_ids,
        "page_obj":products
    }
    return render(request, 'ecommerce/product_list.html',context=context)

def product_detail(request, pk):
    product = Product.objects.filter(pk=pk).first()
    review = Review.objects.filter(product__pk=pk)
    pd = Booking.objects.select_related('order').filter(product__pk=pk)
    paid = True if pd else False
    review_form = ReviewForm()
    cart_form = CartForm(initial={'quantity': 0})

    context = {
        'product':product,
        'review':review,
        'paid':paid,
        'review_form':review_form,
        'cart_form':cart_form
    }

    return render(request,'ecommerce/product_detail.html',context=context)

@login_required
def review_detail(request, pk):
    review = Review.objects.filter(pk=pk)
    comments = Comment.objects.filter(review_id=pk)
    comment_form = CommentForm()

    context = {
        'review':review,
        'comments':comments,
        'comment_form':comment_form,
    }

    return render(request,'ecommerce/review_detail.html',context=context)

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
            return redirect('get-profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'ecommerce/profile.html', context=context)

@login_required
def get_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    favorites = FavoriteProduct.objects.filter(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'favorites':favorites,
    }
    return render(request, 'ecommerce/profile.html', context=context)

@login_required
@transaction.atomic
def cart_add(request, pk):
    cart_form = CartForm(initial={'quantity': 0})

    if request.method == "POST" and request.is_ajax():
        cart_form = CartForm(request.POST)
    else:
        cart_form = 0

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
    
    if cart_form.is_valid():
        if int(cart_form.data["quantity"]) > 0 :
            if int(cart_form.data["quantity"]) + cart_quantity > product_stock:
                messages.add_message(request, messages.INFO, _("Out of stock limit"))
            else:
                if in_cart:
                    in_cart.quantity = int(cart_form.data["quantity"]) + cart_quantity
                    in_cart.save()
                else:
                    product_new = cart_form.save(commit=False)
                    product_new = Cart(user=request.user, product=Product.objects.get(pk=pk), quantity=int(cart_form.data["quantity"]))
                    product_new.save()
                messages.add_message(request, messages.INFO, _('You added a product to your cart'))
                return JsonResponse({"status":200})
        else:
            messages.add_message(request, messages.INFO, _('Please add product quantity more than 0'))
    else:
        errors = cart_form.errors.as_json()
        return JsonResponse({"errors": errors,  "status":400})

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
            context = {
                'system': "Django website team",
                'order_id': order.id,
                'username': order.user.username,
                'date': order.date,
                'orders': cart,
                'total': order.total_price,
                'host': HOST,
            }
            messages.add_message(request, messages.INFO, _('Order is waiting for being approved by admin! Please wait the approve message!'))
            message = get_template('messages/order_success_message.html').render(context)
            msg = EmailMessage(f'New order #{order.id} have been made, please check waiting order.',message, EMAIL_HOST_USER, [EMAIL_HOST_USER],)
            msg.content_subtype = "html"  
            msg.send()
        
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
    orders_list = Order.objects.filter(user=request.user).order_by('-status','-date')
    return render(request, 'ecommerce/order.html', {'order': orders_list})

@login_required
@transaction.atomic
def order_remove(request, pk):
    Order.objects.filter(user=request.user, id=pk).delete()
    messages.add_message(request, messages.INFO, _('Order has been removed')) 

    bookings = Booking.objects.filter(order=pk).select_related('product')
    for item in bookings:
        item.product.quantity += item.quantity
        item.product.save()

    return redirect('/ecommerce/order/')

@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    detail = Booking.objects.filter(order=pk).select_related('product')

    return render(request, 'ecommerce/order_detail.html', {'id': pk, 'status': order.status, 'detail': detail, 'total': order.total_price})

@login_required
def report(request):
    total_orders = Order.objects.all().count()
    total_sales = Order.objects.aggregate(Sum('total_price')).get('total_price__sum', 0)
    max_sales = Order.objects.aggregate(Max('total_price')).get('total_price__max', 0)
    best = {}
    month_price = Order.objects.values_list('date__month').annotate(total=Sum('total_price'))

    if month_price:
        best['month'], best['total_price'] = max(month_price, key=lambda i: i[1])
        best['month_name'] = date(datetime.date(datetime.datetime.now().year, month=best['month'], day=1), 'F')
    
    year = request.GET.get("filter", datetime.datetime.now().year)
    first = Order.objects.filter(date__quarter=1,date__year=year).aggregate(Sum('total_price')).get('total_price__sum', 0)
    second = Order.objects.filter(date__quarter=2,date__year=year).aggregate(Sum('total_price')).get('total_price__sum', 0)
    third = Order.objects.filter(date__quarter=3,date__year=year).aggregate(Sum('total_price')).get('total_price__sum', 0)
    forth = Order.objects.filter(date__quarter=4,date__year=year).aggregate(Sum('total_price')).get('total_price__sum', 0)

    years = Order.objects.dates('date', 'year')

    products = Product.objects.all()

    total =  Booking.objects.values_list('product', flat=True).distinct()

    if 'product_name' in request.GET:
        product_name = request.GET["product_name"]
        products = products.filter(product_name__icontains=product_name)
    
    if 'start' and 'end' in request.GET:
        start = request.GET["start"]
        end = request.GET["end"]
        if start and end:
            b = Booking.objects.filter(order__date__range=[start,end]).values('product').distinct()
            products = Product.objects.filter(pk__in=b)

    context = {
        "total_orders":total_orders,
        "total_sales":total_sales,
        "max_sales":max_sales,
        "best":best,
        "month":month_price,
        "first":first,
        "second":second,
        "third":third,
        "forth":forth,
        'years':years,
        'products':products,
        'total':total,
    }

    return render(request, 'ecommerce/report.html',context=context)


@login_required
@permission_required('ecommerce.can_mark_returned', raise_exception=True)
def order_all_get(request):
    orders = Order.objects.order_by('-status','-date')
    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "order_list":orders,
        "page_obj":page_obj,
    }

    return render(request, 'ecommerce/order_list_all.html',context=context)

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

    detail = Booking.objects.filter(order=pk).select_related('product')

    context = {
        'system': "Django website team",
        'order_id': order.id,
        'username': order.user.username,
        'date': order.date,
        'orders': detail,
        'total': order.total_price,
    }

    if status == 'A':
        messages.add_message(request, messages.INFO, _(f'Order #{pk} have been accepted!'))
        message = get_template('messages/order_accepted_message.html').render(context)
        msg = EmailMessage(f'Your order #{pk} have been accepted.',message, EMAIL_HOST_USER,[order.user.username],)
        msg.content_subtype = "html"  
        msg.send()
    elif  status == 'R':
        messages.add_message(request, messages.INFO, _(f'Order #{pk} have been rejected!'))
        message = get_template('messages/order_rejected_message.html').render(context)
        msg = EmailMessage(f'Your order #{pk} have been rejected.',message, EMAIL_HOST_USER,[order.user.username],)
        msg.content_subtype = "html"  
        msg.send()
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
    
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, 
        'category_list':category_object
    }

    return render(request, 'ecommerce/product_list.html', context=context)

@login_required
def add_favorite_product(request, pk):
    if request.is_ajax():
        in_wishlist = FavoriteProduct.objects.filter(user=request.user, product__pk=pk).first()
        favorite_product_ids = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
        products = Product.objects.all()

        if in_wishlist:
            in_wishlist.delete()
            messages.add_message(request, messages.INFO, _('You deleted a product from your wishlist'))
        else:
            new_obj = FavoriteProduct.objects.create(user=request.user, product_id=pk)        
            new_obj.save()
            messages.add_message(request, messages.INFO, _('You added a product to your wishlist'))
        
        context = {
            "favorite_product_ids":favorite_product_ids,
            "page_obj":products,
            "status":200
        }

        data = {}
        data['list'] = render_to_string('ecommerce/favor_block.html',context=context, request=request)
        return JsonResponse(data)
    
    favorite_product_ids = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request,'ecommerce/product_list.html',{'favorite_product_ids':favorite_product_ids})

@login_required
@transaction.atomic
def review_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
        return redirect(f'/ecommerce/product/{pk}')
    else:
        review_form = ReviewForm(user=request.user, product=product)
        
        context = {
            'review_form': review_form
        }
        return render(request, 'ecommerce/product_detail.html', context=context)

@login_required
@transaction.atomic   
def comment_add(request, pk):
    comment_form = CommentForm()
    if request.method == "POST" and request.is_ajax():
        review = Review.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.review = review
            new_comment.save()

            context = {
                "review_id": new_comment.review.id, 
                "content": new_comment.comment, 
                "id": new_comment.id, 
                "user": new_comment.user.username, 
                "created": new_comment.created, 
                "status":200
            }
            data = {}
            data['list'] = render_to_string('ecommerce/comment_block.html',context=context, request=request)
            return JsonResponse(data)
        else:
            errors = comment_form.errors.as_json()
            return JsonResponse({"errors": errors,  "status":400})

    return render(request,'ecommerce/review_detail.html',{"comment_form": comment_form})

@login_required
@transaction.atomic   
def comment_reply(request, review_pk, cmt_pk):
    comment_form = CommentForm()
    if request.method == "POST" and request.is_ajax():
        review = Review.objects.get(pk=review_pk)
        parent_comment = Comment.objects.get(pk=cmt_pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.review = review
            new_comment.parent_comment = parent_comment
            new_comment.save()

            context = {
                "review_id": new_comment.review.id, 
                "content": new_comment.comment, 
                "id": new_comment.id, 
                "user": new_comment.user.username, 
                "reply_user": parent_comment.user.username,
                "created": new_comment.created, 
                "reply_comment": parent_comment.comment,
                "status":200
            }
            data = {}
            data['list'] = render_to_string('ecommerce/comment_reply_block.html',context=context, request=request)
            return JsonResponse(data)
        else:
            errors = comment_form.errors.as_json()
            return JsonResponse({"errors": errors,  "status":400})

    return render(request,'ecommerce/review_detail.html',{"comment_form": comment_form})

@login_required
def filter_or_export(request):
    if request.method == 'POST':
        if 'filter' in request.POST:
            status = request.POST['export']
            if status != 'All':
                orders = Order.objects.filter(status=status).order_by('-status','-date')
            else:
                orders = Order.objects.order_by('-status','-date')
            paginator = Paginator(orders, 8)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                "order_list":orders,
                "page_obj":page_obj,
                "status":status
            }

            return render(request, 'ecommerce/order_list_all.html',context=context)

        elif 'export-file' in request.POST:
            status = request.POST['export']
            if status != 'All':
                rows = Order.objects.filter(status=status).values_list('id', 'user', 'total_price', 'shipping_address', 'phone_number', 'total_price', 'date', 'status')
            else:
                rows = Order.objects.all().values_list('id', 'user', 'total_price', 'shipping_address', 'phone_number', 'total_price', 'date', 'status')
            
            response = HttpResponse(content_type='application/ms-excel')

            # Name file
            if status == 'All':
                response['Content-Disposition'] = 'attachment; filename="all-orders.xls"'
            elif status == 'A':
                response['Content-Disposition'] = 'attachment; filename="all-approved-orders.xls"'
            elif status == 'W':
                response['Content-Disposition'] = 'attachment; filename="all-waiting-orders.xls"'
            elif status == 'R':
                response['Content-Disposition'] = 'attachment; filename="all-rejected-orders.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Orders')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Order_ID', 'User', 'Total price', 'Shipping address', 'Phone number', 'Total price', 'Date', 'Status']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

def simple_upload(request):
    if request.method == 'POST':
        product_resource = ProductResource()
        dataset = Dataset()
        new_products = request.FILES['myfile']
        
        if new_products.name.split('.')[-1] in ['xls']:
            imported_data = dataset.load(new_products.read(),format='xls')
            for data in imported_data:
                value = Product.objects.create(id=data[0],product_name=data[1],image=data[2],category_id=data[3],description=data[4],price=data[5],quantity=data[6])
                value.save()       
                messages.success(request, _('File is imported sucessfully.'))
                return redirect('get-profile')
        else:
            messages.error(request, _('File is not XLS, please input right excel format form.'))
            return redirect('get-profile')
