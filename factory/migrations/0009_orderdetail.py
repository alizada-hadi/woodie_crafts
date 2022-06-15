# Generated by Django 4.0.5 on 2022-06-15 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0008_order_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.DecimalField(blank=True, decimal_places=2, help_text='بلندی محصول به سانتی متر', max_digits=10, null=True, verbose_name='بلندی محصول')),
                ('width', models.DecimalField(blank=True, decimal_places=2, help_text='عرض محصول به سانتی متر', max_digits=10, null=True, verbose_name='عرض محصول')),
                ('depth', models.DecimalField(blank=True, decimal_places=2, help_text='عمق محصول به سانتی متر', max_digits=10, null=True, verbose_name='عمق محصول')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='تعداد')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price_unit', models.CharField(choices=[('افغانی', 'افغانی'), ('دالر', 'دالر'), ('کلدار', 'کلدار'), ('تومان', 'تومان')], max_length=20, verbose_name='واحد پول')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='مجموع')),
                ('description', models.CharField(help_text='ذکر موارد خاص', max_length=255, verbose_name='توضیحات')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.order')),
            ],
            options={
                'verbose_name': 'جزییات فرمایش',
                'verbose_name_plural': 'جزییات فرمایش',
            },
        ),
    ]
