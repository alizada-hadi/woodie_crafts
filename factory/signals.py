from django.db.models.signals import post_save, post_delete
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
    if created:
        
        order = Order.objects.get(id=instance.order.id)
        order.amount -= instance.receive_amount
        receive = ReceiveMoney.objects.get(id=instance.id)
        receive.remain_amount = instance.order.amount - instance.receive_amount
        receive.save()
        order.save()
    elif not created:
        order = Order.objects.get(id=instance.order.id)
        order.amount = 0
        for item in order.receivemoney_set.all():
            order.amount += item.remain_amount * instance.receive_amount
        order.save()


@receiver(post_delete, sender=ReceiveMoney)
def receive_delete_money(sender, instance, *args, **kwargs):
    order = Order.objects.get(id=instance.order.id)
    order.amount = order.amount + instance.receive_amount
    order.save()
