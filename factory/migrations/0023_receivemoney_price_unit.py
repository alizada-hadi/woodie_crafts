# Generated by Django 4.0.5 on 2022-06-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0022_receivemoney_remain_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivemoney',
            name='price_unit',
            field=models.CharField(choices=[('افغانی', 'افغانی'), ('دالر', 'دالر'), ('کلدار', 'کلدار'), ('تومان', 'تومان')], default='دالر', max_length=20, verbose_name='واحد پول'),
        ),
    ]
