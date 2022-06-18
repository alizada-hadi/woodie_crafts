from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import  (
    Order, 
    OrderDetail, 
    ReceiveMoney, 
    Employee, 
    EmployeeWork, 
    EmployeeSalaryPayment
)


@receiver(post_save, sender=OrderDetail)
def create_order_detail(sender, instance, created, *args, **kwargs):
    if created:
        order = Order.objects.get(id=instance.order.id)
        order.amount += instance.price * instance.qty
        order.save()
    elif not created:
        order = Order.objects.get(id=instance.order.id)
        order.amount = 0
        for item in order.orderdetail_set.all():
            order.amount += item.price * item.qty
        order.save()

@receiver(post_delete, sender=OrderDetail)
def delete_order_detail(sender, instance, *args, **kwargs):
    if not instance.id:
        order.amount = 0
        order.save()
    else:
        order = Order.objects.get(id=instance.order.id)
        order.amount -= instance.price * instance.qty
        order.save()


@receiver(post_save, sender=ReceiveMoney)
def receive_create_money(sender, instance, created, *args, **kwargs):
    if created:
        order = Order.objects.get(id=instance.order.id)
        order.amount -= instance.receive_amount
        receive = ReceiveMoney.objects.get(id=instance.id)
        receive.remain_amount = instance.order.amount - instance.receive_amount
        receive.save()
        order.save()

    if not created:
        order = Order.objects.get(id=instance.order.id)
        receive = ReceiveMoney.objects.get(id=instance.id)
        order.amount = 0 # in this case value is 3000
        for item in order.orderdetail_set.all():
            order.amount += item.price * item.qty
        x = 0
        for i in order.receivemoney_set.all():
            x += i.receive_amount
        order.amount -= x 
        receive.remain_amount -= x
        order.save()



@receiver(post_delete, sender=ReceiveMoney)
def receive_delete_money(sender, instance, *args, **kwargs):
    order = Order.objects.get(id=instance.order.id)
    order.amount = order.amount + instance.receive_amount
    order.save()



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