# Generated by Django 4.2.6 on 2023-11-02 21:03

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='provider_id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=11, unique=True),
        ),
    ]
