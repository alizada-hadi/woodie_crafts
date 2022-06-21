from functools import total_ordering
from django.contrib import admin
from .models import EmployeeSalaryPayment, EmployeeWork, Employee, EmployeeAttendance
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from django.utils.html import format_html, urlencode
from django.db.models import Count
from django.urls  import reverse
from django.utils.safestring import mark_safe
from django_admin_inline_paginator.admin import TabularInlinePaginated



def employee_work(obj):
    url = reverse("employee:employee_work_detail", args=[obj.id])
    return mark_safe(f"<a href='{url}'>نمایش</a>")

employee_work.short_description = "لیست کارکرد ها"




# employee admin
@admin.register(Employee)
class EmployeeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')
    list_display = ("first_name", "last_name", "phone_number", "position", "address", "emp_type", "salary", employee_work, )
    list_filter = ["address", "emp_type", "salary", "position", "created_at"]
    search_fields = ("first_name", "last_name", "emp_type", "phone_number", "address", )
    list_editable = ["emp_type"]
    readonly_fields = ["total_work"]
    list_per_page = 10
    fieldsets = (
        ("مشخصات کارمند", {
            "fields" : [("first_name", "last_name", "emp_type", ), ("phone_number", "address", "position",), ("created_at",), ("total_work",),]
        }), 
        ("معاش کارمند", {
            "fields" : ["salary"], 
            "classes" : ("collapse",)
        }),
    )


# employee work
@admin.register(EmployeeWork)
class EmployeeWorkAdminRegister(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.assigned_date).strftime('%Y/%m/%d')
        
    get_created_jalali.short_description = "تاریخ کار"
    autocomplete_fields = ["employee"]
    raw_id_fields = ["order_detail"]
    list_display = ["employee", "order_detail", "qty", "fees", "done", "get_created_jalali"]
    search_fields = ["work", "employee",  "order_detail"]
    list_filter = ["employee", "order_detail", "done", "assigned_date"]
    list_per_page = 10

    fields = [("employee", "order_detail", "qty"), ("fees", "done", "assigned_date")]





@admin.register(EmployeeSalaryPayment)
class EmployeeSalaryPaymentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.paid_at).strftime('%Y/%m/%d')
    get_created_jalali.short_description = "تاریخ"
    def total_work(obj): # employee
        total = 0
        for i in obj.employee.employeework_set.all():
            total += i.fees * i.qty
        return total

    total_work.short_description = "مجموع کارکرد"

    fieldsets = (
        ("تفصیل حسابات", {
            "fields" : [("employee", "work", "paid_amount", "paid_at", ), ("description", )]
        }), 
    )

    autocomplete_fields = ["employee"]
    raw_id_fields = ["work"]

    list_display = ["employee", "work", total_work, "paid_amount", "remain_amount", "get_created_jalali"]
    list_filter = ["employee", "work", "paid_at"]
    search_fields = ["employee", "paid_amount", "remain_amount"]
    list_per_page = 10
    date_hierarchy = "paid_at"



@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')
    get_created_jalali.short_description = "تاریخ"
    
    list_display = ["employee", "status", "delay", "penalty", "get_created_jalali"]
    list_filter = ["employee", "status", "delay", "date"]
    list_editable = ["status", "delay", "penalty"]
    search_fields = ["employee"]
    list_per_page = 10
    autocomplete_fields = ["employee"]
    fieldsets = (
        ("حاضری کارمندان", {
            "fields" : [("employee", "status", "delay", "penalty", "date"),]
        }), 
    )