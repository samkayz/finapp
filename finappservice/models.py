from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    officeid = models.IntegerField()
    roleid = models.IntegerField()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'last_name', 'password', 'officeid', 'roleid']
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

    def get_username(self):
        return self



class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'role'


class Office(models.Model):
    name = models.CharField(max_length=255)
    opening_date = models.CharField(max_length=255)
    parentid = models.IntegerField()

    class Meta:
        db_table = 'office'