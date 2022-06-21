from tabnanny import verbose
from django.db import models



class Expense(models.Model):
    UNIT = (
        ("دالر", "دالر"),
        ("افغانی", "افغانی"),
        ("کلدار", "کلدار"),
        ("تومان", "تومان"),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان مصرف")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار کل پرداختی")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار پرداخت شده")
    amount_letter = models.CharField(max_length=200, verbose_name="مقدار پرداختی به حروف")
    expense_unit = models.CharField(max_length=20, choices=UNIT, default="افغانی", verbose_name="واحد پولی")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار باقی مانده")
    expenser = models.CharField(max_length=200, verbose_name="مصرف کننده")
    date = models.DateField(verbose_name="تاریخ مصرف")


    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "مصرف"
        verbose_name_plural = "مصارف"



class Income(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان آمد")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار آمد")
    date = models.DateField(verbose_name="تاریخ آمد")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "درآمد"
        verbose_name_plural = "ٔدرآمد"