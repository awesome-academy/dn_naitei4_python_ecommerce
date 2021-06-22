from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile', views.update_profile, name='user-page'),
    path('wishlist', views.add_to_wishlist, name='wishlist')
]
