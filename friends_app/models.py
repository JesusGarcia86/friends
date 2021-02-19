from django.db import models
import re
from datetime import date, datetime

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="Name must be longer than 2 characters!"
        if len(postdata['l_n'])<2:
            errors['l_n']="Alias must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be a valid format!"
        if len(postdata['pw'])<8:
            errors['pw']="Password must be at least 8 characters!"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw']="Password and confirm password must match!"
        if postdata['bh']:
            num = datetime.strptime(postdata["bh"], '%Y-%m-%d') - datetime.today()
            if abs(abs(num.days)/365) < 16:
                errors['bh']="You must be 16 to register!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)