# Generated by Django 3.1.4 on 2021-04-16 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0004_auto_20210328_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_head_teller',
            field=models.BooleanField(default=False, verbose_name='is_head_teller'),
        ),
    ]