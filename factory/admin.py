from django.contrib import admin
from .models import Customer, ProductCategory, Order, OrderDetail
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from django.utils.html import format_html, urlencode
from django.db.models import Count
from django.urls  import reverse
# Register your models here.

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    list_display = ["order", "height", "width", "depth", "direction", "qty", "price"]
    list_filter = ["direction", "price", "height", "width", "depth"]
    search_fields = ["height", "width", "direction"]





class OrderDetailInline(admin.StackedInline):
    fieldsets = (
        ("تفصیلات", {
            "fields" : [("product","qty", "price", "price_unit", "description", )], 
            "classes" : ('wide', 'extrapretty',)
            
        }),
        ("اندازه محصول", {
            "fields" : [("height", "width", "depth", "direction", )], 
            "classes" : ('collapse', ), 
            "description" : "در بعضی از فرمایشات مشتری شما نیاز ندارید اندازه محصول را حتما داشته باشید. لذا این بخش اختیاری می باشد. "
        }),
    )
    model = OrderDetail
    raw_id_fields = ('product', )
    exclude = ["total"]
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [OrderDetailInline]
    
    
    fields = [("customer", "status", "order_date", )]
    raw_id_fields = ("customer", )
    list_display = ["customer", "status", "order_date", "order_detail_count", "total_cost"]
    list_filter = ["customer", "status", "order_date"]
    search_fields = ["customer", "product"]
    list_editable = ["status", "order_date"]
    list_per_page = 10


    def order_detail_count(self, order):
        return order.order_detail_count

    def total_cost(self, order):
        total = 0
        for i in order.orderdetail_set.all():
            total += i.price * i.qty
        return total
    total_cost.short_description = "مجمول پول"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_detail_count = Count("orderdetail")
        )
    order_detail_count.short_description = "تعداد اقلام فرمایش داده شده"


    def get_created_jalali(self, obj):
        return date2jalali(obj.order_date).strftime('%Y/%m/%d')
    get_created_jalali.short_description = "تاریخ ثبت فرمایش"





@admin.register(Customer)
class CustomerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.created).strftime('%y/%m/%d')
    list_display = ["first_name", "last_name", "phone_number1", "phone_number2", "created", "number_of_order"]
    list_filter = ["created"]
    search_fields = ["first_name", "last_name", "address"]
    list_editable = ["created"]
    date_hierarchy = 'created'

    @admin.display(ordering="number_of_order")
    def number_of_order(self, customer):
        url = (
            reverse("admin:factory_order_changelist")
            + '?'
            + urlencode({
                'customer__id' : str(customer.id)
            })
            )
        return format_html('<a href="{}">{}</a>', url, customer.number_of_order)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
         number_of_order = Count("order")  
        )
    
    number_of_order.short_description = "تعداد کل فرمایشات"

    


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src={} />'.format(obj.sample_image.url))
    image_tag.short_description = "نمونه عکس"

    def get_created_jalali(self, obj):
        return date2jalali(obj.created).strftime('%Y/%m/%d')
    get_created_jalali.short_description = 'تاریخ ایجاد'


    list_display = ["category_name", "image_tag", "get_created_jalali"]
    search_fields = ["product"]