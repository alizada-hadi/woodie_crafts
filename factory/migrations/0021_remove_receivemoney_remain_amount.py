# Generated by Django 4.0.5 on 2022-06-17 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0020_alter_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receivemoney',
            name='remain_amount',
        ),
    ]