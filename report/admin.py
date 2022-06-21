from django.contrib import admin
from .models import Expense, Income
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali, date2jalali




@admin.register(Expense)
class ExpenseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')
    get_created_jalali.short_description = "تاریخ مصرف"

    list_display = ["title", "total", "amount", "expense_unit", "remain_amount", "get_created_jalali"]
    list_filter = ["title", "total", "date", "expense_unit"]
    search_fields = ["title", "expenser"]
    list_editable = ["total", "amount", "remain_amount", "expense_unit"]
    list_per_page = 10
    fields = [("title", "total", "amount", "amount_letter", "expense_unit"), ("remain_amount", "expenser", "date")]


@admin.register(Income)
class IncomeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def get_created_jalali(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')
    get_created_jalali.short_description = "تاریخ ثبت"
    list_display = ["title", "amount", "get_created_jalali"]
    list_filter = ["title", "amount", "date"]
    list_per_page = 10
    search_fields = ["title", "amount"]
    list_editable = ["amount"]
    fields = [("title", "amount", "date")]