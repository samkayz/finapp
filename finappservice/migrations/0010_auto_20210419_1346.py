# Generated by Django 3.1.4 on 2021-04-19 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finappservice', '0009_loantype_loan_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanapplication',
            old_name='loanType',
            new_name='loan_code',
        ),
    ]