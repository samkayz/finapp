# Generated by Django 3.1.4 on 2021-04-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0017_auto_20210421_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='internaltransacthistory',
            name='date_created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
