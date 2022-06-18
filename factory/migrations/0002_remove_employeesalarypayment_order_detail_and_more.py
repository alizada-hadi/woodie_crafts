# Generated by Django 4.0.5 on 2022-06-18 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeesalarypayment',
            name='order_detail',
        ),
        migrations.AddField(
            model_name='employeesalarypayment',
            name='work',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='factory.employeework', verbose_name='بابت کار'),
            preserve_default=False,
        ),
    ]