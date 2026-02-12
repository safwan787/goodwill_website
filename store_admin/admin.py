from django.contrib import admin
from .models import*
# Register your models here.




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    list_editable = ('stock', 'available')
    search_fields = ('name',)
    list_editable = ('available',)




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

from .models import Inquiry, InquiryAttachment

class InquiryAttachmentInline(admin.TabularInline):
    model = InquiryAttachment
    extra = 0

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    inlines = [InquiryAttachmentInline]

admin.site.register(InquiryAttachment)
