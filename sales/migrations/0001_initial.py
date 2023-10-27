# Generated by Django 4.2.6 on 2023-10-26 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.main


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_id', models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=11, unique=True)),
                ('date_sale', models.DateTimeField(auto_now_add=True)),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas_realizadas', to='employee.employee')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas_realizadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('id_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_sales', to='products.productdatageneral')),
                ('id_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
        ),
    ]
