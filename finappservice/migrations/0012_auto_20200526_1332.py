# Generated by Django 3.0.6 on 2020-05-26 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0011_auto_20200526_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tellerbalance',
            name='bal',
            field=models.FloatField(),
        ),
    ]