from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile', views.update_profile, name='user-page'),
    path('cart/', views.cart_get, name='cart_get'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/increase/<int:pk>/', views.increase_product_in_cart, name='increase-product-in-cart'),
    path('cart/decrease/<int:pk>/', views.decrease_product_in_cart, name='decrease-product-in-cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('order/', views.order_get, name='order_get'),
    path('order/detail/<int:pk>', views.order_detail, name='order_detail'),
    path('order/all/', views.OrderAllListView.as_view(), name='all-order'), 
    path('order/check/<int:pk>', views.check_order_status, name='check-order-status'), 
]
