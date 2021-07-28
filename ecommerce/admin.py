from ecommerce.models import Cart, Category, Comment, FavoriteProduct, Order, Product, Profile, Review, User
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Category)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product_name','image','display_category','description','publish_date','price','quantity')
    list_filter = ('publish_date',)

    def display_category(self, obj):
        return obj.category.name
    
    display_category.short_description = 'Category'

class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
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

class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_user','display_product','display_review','comment')

    def display_user(self, obj):
        return obj.user.username

    def display_product(self, obj):
        return obj.review.product.product_name

    def display_review(self, obj):
        return obj.review.title

    display_product.short_description = 'Product name'
    display_review.short_description = 'Review title'

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
