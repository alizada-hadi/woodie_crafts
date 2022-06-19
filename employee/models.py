from django.db import models
from factory.models import Order, OrderDetail
# Create your models here.


class Employee(models.Model):
    EMPLOYEE_TYPE = (
        ("کونترات", "کونترات"),
        ("ماهوار", "ماهوار")
    )
    first_name = models.CharField(max_length=200, verbose_name="نام")
    last_name = models.CharField(max_length=200, verbose_name="تخلص")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.CharField(max_length=200, verbose_name="آدرس خانه")
    position = models.CharField(max_length=200, verbose_name="نوع کارمند")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True, verbose_name="معاش")
    total_work = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مجموع کارکرد مشتری")
    emp_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE, verbose_name="نوعیت معاش")
    created_at = models.DateField(verbose_name="تاریخ استخدام")



    def __str__(self) -> str:
        return self.first_name

    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"


class EmployeeWork(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, verbose_name="کارکرد")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="کارمند")
    qty = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="تعداد کار")
    fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="دستمزد فی واحد کار")
    done = models.BooleanField(default=False, verbose_name="تکمیل شده")
    assigned_date = models.DateField(verbose_name="تاریخ کار", null=True, blank=True)


    def __str__(self):
        return f"{self.order_detail.product.category_name}"

    class Meta:
        verbose_name = "کارکرد کارمند"
        verbose_name_plural = "کارکرد کارمندان"

class EmployeeSalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="کارمند")
    work = models.ForeignKey(EmployeeWork, on_delete=models.CASCADE, verbose_name="بابت کار")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مساعده")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="باقی مانده")
    paid_at = models.DateField(verbose_name="تاریخ پرداخت")


    def __str__(self) -> str:
        return f"دریافتی های آقای {self.employee.first_name} {self.employee.last_name}"

    class Meta:
        verbose_name = "حساب کارمندان"
        verbose_name_plural = "حساب کارمندان"
