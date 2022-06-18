from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import  Order, OrderDetail, ReceiveMoney

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
    if not instance._state.adding:
        print("this is an update ")
    else:
        print("this is a create ")
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
