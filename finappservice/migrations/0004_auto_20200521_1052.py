# Generated by Django 3.0.6 on 2020-05-21 10:52

from django.db import migrations, models
import finappservice.function


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0003_addresstable_customer_identificationid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customerId',
            field=models.CharField(blank=True, default=finappservice.function.customerId, max_length=255, null=True),
        ),
    ]
