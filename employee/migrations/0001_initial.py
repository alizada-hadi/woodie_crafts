# Generated by Django 4.0.5 on 2022-06-19 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('factory', '0004_remove_employeesalarypayment_employee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='نام')),
                ('last_name', models.CharField(max_length=200, verbose_name='تخلص')),
                ('phone_number', models.CharField(max_length=20, verbose_name='شماره تماس')),
                ('address', models.CharField(max_length=200, verbose_name='آدرس خانه')),
                ('position', models.CharField(max_length=200, verbose_name='نوع کارمند')),
                ('salary', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='معاش')),
                ('total_work', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='مجموع کارکرد مشتری')),
                ('emp_type', models.CharField(choices=[('کونترات', 'کونترات'), ('ماهوار', 'ماهوار')], max_length=20, verbose_name='نوعیت معاش')),
                ('created_at', models.DateField(verbose_name='تاریخ استخدام')),
            ],
            options={
                'verbose_name': 'کارمند',
                'verbose_name_plural': 'کارمندان',
            },
        ),
        migrations.CreateModel(
            name='EmployeeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='تعداد کار')),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='دستمزد فی واحد کار')),
                ('done', models.BooleanField(default=False, verbose_name='تکمیل شده')),
                ('assigned_date', models.DateField(blank=True, null=True, verbose_name='تاریخ کار')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.employee', verbose_name='کارمند')),
                ('order_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.orderdetail', verbose_name='کارکرد')),
            ],
            options={
                'verbose_name': 'کارکرد کارمند',
                'verbose_name_plural': 'کارکرد کارمندان',
            },
        ),
        migrations.CreateModel(
            name='EmployeeSalaryPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='مساعده')),
                ('remain_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='باقی مانده')),
                ('paid_at', models.DateField(verbose_name='تاریخ پرداخت')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.employee', verbose_name='کارمند')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeework', verbose_name='بابت کار')),
            ],
            options={
                'verbose_name': 'حساب کارمندان',
                'verbose_name_plural': 'حساب کارمندان',
            },
        ),
    ]
