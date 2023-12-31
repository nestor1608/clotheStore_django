# Generated by Django 4.2.6 on 2023-11-02 21:03

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productdatageneral',
            old_name='Article',
            new_name='article',
        ),
        migrations.AddField(
            model_name='productdatageneral',
            name='gener',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unisex', 'Unisex')], default='male', max_length=7),
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
