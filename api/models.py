from django.db import models

# Create your models here.


class User(models.Model):

    username = models.CharField(max_length=32)  # varchar(32)
    password = models.CharField(max_length=32)  # varchar(32)


class Department(models.Model):

    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
