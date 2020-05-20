from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    officeid = models.IntegerField()
    roleid = models.IntegerField()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'last_name', 'password']
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

    def get_username(self):
        return self