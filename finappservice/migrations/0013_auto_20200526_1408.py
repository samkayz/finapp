# Generated by Django 3.0.6 on 2020-05-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0012_auto_20200526_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='receiverAccount',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='receiverName',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='senderAccount',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='senderName',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]