from __future__ import absolute_import, unicode_literals 
from celery.schedules import crontab
from celery import shared_task
from celery.task import periodic_task
from .models import *
import string
import random
from datetime import datetime
import time
from datetime import timedelta
import os
from django.shortcuts import get_object_or_404
from . models import *
from . function import App


newapp = App()
base_date_time = datetime.now()
today = (datetime.strftime(base_date_time, "%Y-%m-%d"))


@periodic_task(run_every=timedelta(seconds=300))
def hello():
    print("Welcome to Celery")
    pass



@periodic_task(run_every=timedelta(seconds=5))
def checkLoanExpiringDate():
    import datetime
    now = datetime.datetime.strptime(today, "%Y-%m-%d").date()
    all_loan = LoanApplication.objects.filter()
    for loans in all_loan:
        account_detail = get_object_or_404(Account, accounNumber=loans.accountNumber, customerId=loans.customerId)
        if account_detail.workingBalance == 0.0: continue
        if loans.loan_paid == True: continue
        if loans.pay_day > now: continue
        
        ## Check The Account for Loan
        
        if loans.loanAmount > account_detail.workingBalance:
            ## Do Calculation
            to_pay = loans.loanAmount - account_detail.workingBalance
            
            amount = loans.loanAmount - to_pay
            ## Update Loan
            updateLoan = LoanApplication.objects.filter(loanId=loans.loanId)
            updateLoan.update(loanBal=to_pay)
            
            ## Update Account
            updateAccount = Account.objects.filter(accounNumber=loans.accountNumber, customerId=loans.customerId)
            updateAccount.update(previousBalance=account_detail.workingBalance, workingBalance=0)
            
            newapp.createLog(amount, loans.customerName, loans.accountNumber, receiverName='Loan Repayment', receiverAccount='Loan Repayment', comment='Loan Repayment')
        
        else: 
            ## Do Calculation
            bal =  account_detail.workingBalance - loans.loanAmount
            
            ## Update Loan
            updateLoan = LoanApplication.objects.filter(loanId=loans.loanId)
            updateLoan.update(loanBal=0, loan_paid=True)
            
            ## Update Account
            updateAccount = Account.objects.filter(accounNumber=loans.accountNumber, customerId=loans.customerId)
            updateAccount.update(previousBalance=account_detail.workingBalance, workingBalance=bal)
            
            newapp.createLog(loans.loanAmount, loans.customerName, loans.accountNumber, receiverName='Loan Repayment', receiverAccount='Loan Repayment', comment='Loan Repayment')
        
    
    pass
            
        
        
        