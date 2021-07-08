from ecommerce.models import Booking, Cart, Category, FavoriteProduct, Order, Product, Profile, Review, User
from django.contrib import admin

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','image','display_category','description','publish_date','price','quantity')
    list_filter = ('publish_date',)

    def display_category(self, obj):
        return obj.category.name
    
    display_category.short_description = 'Category'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('display_user','total_price','date','status')
    list_filter = ('date','status')
    
    def display_user(self, obj):
        return obj.user.username
    
    display_user.short_description = 'User'

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('display_user','product')
    list_filter = ('user','product')

    def display_user(self, obj):
        return obj.user.username

    display_user.short_description = 'User'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('display_user','birthday','address')

    def display_user(self, obj):
        return obj.user.username
    
    display_user.short_description = 'User'

class CartAdmin(admin.ModelAdmin):
    list_display = ('display_product','quantity')

    def display_product(self, obj):
        return obj.product.product_name
    
    display_product.short_description = 'Product name'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('display_user','display_product','title','content','rate','created')
    list_filter = ('created','rate')

    def display_user(self, obj):
        return obj.user.username

    def display_product(self, obj):
        return obj.product.product_name
    
    display_user.short_description = 'User'
    display_product.short_description = 'Product name'

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Review, ReviewAdmin)

