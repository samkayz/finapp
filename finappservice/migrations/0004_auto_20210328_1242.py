# Generated by Django 3.1.4 on 2021-03-28 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0003_auto_20210328_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='finappservice.customer'),
        ),
    ]