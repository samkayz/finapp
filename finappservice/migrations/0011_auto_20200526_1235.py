# Generated by Django 3.0.6 on 2020-05-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0010_teller_tellerbalance_tellertransactionhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='tellerbalance',
            name='bal',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tellerbalance',
            name='closeBal',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tellerbalance',
            name='closeDate',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='tellerbalance',
            name='totaltran',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
