# Generated by Django 3.0.6 on 2020-05-28 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0017_loanapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='loanType',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]