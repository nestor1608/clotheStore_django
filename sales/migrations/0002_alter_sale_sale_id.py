# Generated by Django 4.2.6 on 2023-10-26 16:56

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=11, unique=True),
        ),
    ]
