from decimal import Decimal
from tabnanny import verbose
from this import d
from django.db import models
from PIL import Image


class Customer(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="نام مشتری")
    last_name = models.CharField(max_length=200, verbose_name="تخلص")
    phone_number1 = models.CharField(max_length=15, verbose_name="شماره تماس")
    phone_number2 = models.CharField(max_length=15, null=True, blank=True, verbose_name="شماره واتساپ یا تلگرام")
    address = models.TextField(verbose_name="آدرس مشتری")
    created = models.DateField(verbose_name="تاریخ مراجعه")

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"



class ProductCategory(models.Model):
    category_name = models.CharField(max_length=200, verbose_name="نام محصول")
    sample_image = models.ImageField(upload_to="category/images", null=True, blank=True, verbose_name="نمونه عکس")
    created = models.DateField(verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "کتگوری محصولات"
        verbose_name_plural = "کتگوری محصولات"

    def __str__(self) -> str:
        return self.category_name

    def save(self):
        super().save()

        img = Image.open(self.sample_image.path)
        
        if img.height > 100 or img.width > 100:
            output_size = (100,100)
            img.thumbnail(output_size)
            img.save(self.sample_image.path)

class Order(models.Model):
    ORDER_STATUS = (
        ("جدید", "جدید"),
        ("در حال اجرا", "در حال اجرا"),
        ("تمام", "تمام"),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, verbose_name="نام مشتری")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="جدید", verbose_name="وضعیت فرمایش")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,  verbose_name="مقدار باقی مانده")
    order_date = models.DateField(verbose_name="تاریخ فرمایش")


    class Meta:
        verbose_name = "فرمایش"
        verbose_name_plural = 'فرمایشات'

    def __str__(self) -> str:
        return f" مشتری {self.customer.first_name} {self.customer.last_name}"


class OrderDetail(models.Model):
    PRICE_UNIT = (
        ("افغانی", "افغانی"), 
        ("دالر",  "دالر"),
        ("کلدار",  "کلدار"),
        ("تومان",  "تومان"),
    )
    DIRECTION = (
        ("راست", "راست"),
        ("چپ", "چپ"),
    )
    product = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, verbose_name="کتگوری محصول", null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="فرمایش دهنده")
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="بلندی محصول")
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="عرض محصول")
    depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="عمق محصول")
    direction = models.CharField(max_length=30, choices=DIRECTION, default="راست", null=True,  blank=True, verbose_name="سمت")
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="تعداد یا متراژ")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="قیمت")
    price_unit = models.CharField(max_length=20, choices=PRICE_UNIT, verbose_name="واحد پول", default="افغانی")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مجموع")
    description = models.CharField(max_length=255, verbose_name="توضیحات", help_text="ذکر موارد خاص")

    def __str__(self) -> str:
        return f" {self.qty} {self.product.category_name} از {self.order.customer.first_name} {self.order.customer.last_name}"
    
    class Meta:
        verbose_name = "جزییات فرمایش"
        verbose_name_plural = "جزییات فرمایش"

    def total_cost(self):
        return self.price * self.qty



"""
Recieve money from customers for specific orders
"""
class ReceiveMoney(models.Model):
    PRICE_UNIT = (
        ("افغانی", "افغانی"), 
        ("دالر",  "دالر"),
        ("کلدار",  "کلدار"),
        ("تومان",  "تومان"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="دریافتی از مشتری")
    receive_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار اخذ شده")
    price_unit = models.CharField(max_length=20, choices=PRICE_UNIT, default="دالر", verbose_name="واحد پول")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار باقی مانده")
    receive_date = models.DateField(verbose_name="تاریخ اخذ پول")


    class Meta:
        verbose_name = "دریافتی"
        verbose_name_plural = "دریافتی ها"
    
    def __str__(self) -> str:
        return f"دریافتی از {self.order.customer.first_name} {self.order.customer.last_name}"


# employee model

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



# employee work

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
        verbose_name_plural = "کارکرد کارمند"


class EmployeeSalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="کارمند")
    work = models.ForeignKey(EmployeeWork, on_delete=models.CASCADE, verbose_name="بابت کار")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مساعده")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="باقی مانده")
    paid_at = models.DateField(verbose_name="تاریخ پرداخت")


    def __str__(self) -> str:
        return f"دریافتی های آقای {self.employee.first_name} {self.employee.last_name}"

    class Meta:
        verbose_name = "حسابات کارمند"
        verbose_name_plural = "حسابات کارمند"