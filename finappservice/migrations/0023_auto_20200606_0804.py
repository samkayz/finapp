# Generated by Django 3.0.6 on 2020-06-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0022_auto_20200606_0803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='doc',
        ),
        migrations.AddField(
            model_name='identificationid',
            name='doc',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='customer/%Y/%M/%D/'),
        ),
    ]