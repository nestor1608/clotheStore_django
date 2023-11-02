# Generated by Django 4.2.6 on 2023-11-02 00:28

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdatageneral',
            name='imagen_url',
        ),
        migrations.AddField(
            model_name='productdatageneral',
            name='img',
            field=models.ImageField(default=1, upload_to='media/product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productcost',
            name='product_cost_id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='productdatageneral',
            name='product_id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=11, unique=True),
        ),
    ]