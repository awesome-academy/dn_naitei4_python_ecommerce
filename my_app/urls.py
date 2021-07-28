"""my_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ecommerce.views import APICheckoutView, APIProductViewSet, APIUserLoginView, APIUserRegisterView, OrderList
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Simple API",
        default_version='v1',
        description="An simple API for CRUD with Article",
        contact=openapi.Contact(email="contact@education.sun.local"),
        license=openapi.License(name="Sun Education License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecommerce/', include('ecommerce.urls')),
    path('', RedirectView.as_view(url='ecommerce/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password.done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete',),
    path('api-auth/', include('rest_framework.urls')),
    path('api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/checkout/', APICheckoutView.as_view(), name='checkout'),
    path("api/order/", OrderList.as_view(), name="orders_list"),
    path('api/register/', APIUserRegisterView.as_view(), name='register'),
    path('api/login/', APIUserLoginView.as_view(), name='login'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register('products', APIProductViewSet, basename='products')
urlpatterns += router.urls
