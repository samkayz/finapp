# Generated by Django 3.1.4 on 2020-12-23 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0027_auto_20200606_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
