# Generated by Django 3.0.6 on 2020-05-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0014_auto_20200528_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tellerbalance',
            name='closeBal',
            field=models.FloatField(default='0'),
        ),
        migrations.AlterField(
            model_name='tellerbalance',
            name='openBal',
            field=models.FloatField(),
        ),
    ]
