from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price','digital','category', 'description')
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(About, AboutAdmin)