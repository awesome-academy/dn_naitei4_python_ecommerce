from ecommerce.models import Booking, Category, FavoriteProduct, Order, Product, User
from django.contrib import admin

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','image','display_category','description','publish_date','price','quantity')
    list_filter = ('publish_date',)

    def display_category(self, obj):
        return obj.category.name
    
    display_category.short_description = 'Category'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','image','birthday','address','role')
    list_filter = ('role',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('display_user','display_product','total_price','date','status')
    list_filter = ('date','status')
    
    def display_user(self, obj):
        return obj.user.username
    
    def display_product(self,obj):
        return obj.product.product_name
    
    display_user.short_description = 'User'
    display_product.short_description = 'Product'

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('display_user','product')
    list_filter = ('is_favorited','user','product')

    def display_user(self, obj):
        return obj.user.username

    display_user.short_description = 'User'

admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)

