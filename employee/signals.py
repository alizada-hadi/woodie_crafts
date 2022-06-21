from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import  (
    Employee,
    EmployeeAttendance, 
    EmployeeWork, 
    EmployeeSalaryPayment
)
from report.models import Expense


@receiver(post_save, sender=Employee)
def employee_create(sender, instance, created, *args, **kwargs):
    if created:
        instance.total_work = instance.salary
        instance.save()



# apply penalty for employee if they are absent
@receiver(post_save, sender=EmployeeAttendance)
def employee_attandence_create(sender, instance, created, *args, **kwargs):
    if created:
        employee = Employee.objects.get(id=instance.employee.id)
        employee.total_work -= instance.penalty
        employee.save()
    
    if not created:
        total = 0
        employee =  Employee.objects.get(id=instance.employee.id)
        employee.total_work = employee.salary
        for i in employee.employeeattendance_set.all():
            total += i.penalty
        employee.total_work -= total
        employee.save()

@receiver(post_delete, sender=EmployeeAttendance)
def employee_attandence_delete(sender, instance, *args, **kwargs):
    total = 0
    employee =  Employee.objects.get(id=instance.employee.id)
    employee.total_work = employee.salary
    for i in employee.employeeattendance_set.all():
        total += i.penalty
    employee.total_work -= total
    employee.save()


@receiver(post_save, sender=EmployeeWork)
def employee_work_create(sender, instance, created, *args, **kwargs):
    if created:
        employee = Employee.objects.get(id=instance.employee.id)
        employee.total_work += instance.qty * instance.fees
        employee.save()

    if not created:
        employee = Employee.objects.get(id=instance.employee.id)
        employee.total_work = 0
        for item in employee.employeework_set.all():
            employee.total_work += item.fees * item.qty
        employee.save()



@receiver(post_delete, sender=EmployeeWork)
def employee_work_delete(sender, instance, *args, **kwargs):
    employee = Employee.objects.get(id=instance.employee.id)
    employee.total_work -= instance.qty * instance.fees
    employee.save()


@receiver(post_save, sender=EmployeeSalaryPayment)
def employee_salary_payment_create(sender, instance, created, *args, **kwargs):
    if created:
        employee = Employee.objects.get(id=instance.employee.id)
        Expense.objects.create(
            title="معاش کارمند", 
            total=employee.salary, 
            amount=instance.paid_amount, 
            amount_letter = "", 
            expense_unit = "افغانی",  
            remain_amount=employee.salary - instance.paid_amount, 
            expenser = "مدیر", 
            date = instance.paid_at
        )
        instance.remain_amount = employee.total_work - instance.paid_amount
        employee.total_work -= instance.paid_amount
        instance.save()
        employee.save()
    if not created:
        employee = Employee.objects.get(id=instance.employee.id)
        total = 0
        for i in employee.employeework_set.all():
            total += i.fees * i.qty
        employee.total_work = total - instance.paid_amount
        employee.save()


@receiver(post_delete, sender=EmployeeSalaryPayment)
def employee_salary_payment_delete(sender, instance, *args, **kwargs):
    employee = Employee.objects.get(id=instance.employee.id)
    employee.total_work += instance.paid_amount
    employee.save()