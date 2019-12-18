from django.db import models
from django.contrib import messages
import bcrypt
import re
from datetime import datetime, time, date
from time import strftime

class Usermanager(models.Manager):
    def user_validator(self, formInfo):
        filterResult = User.objects.filter(username=formInfo['username'])
        errors = {}
        username_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]')
        usernameMatch = User.objects.filter(username = formInfo['username'])
        # if len(usernameMatch) > 0:
        #     errors['usernameTaken'] = "This username is already Taken"
        if len(formInfo['name']) < 3 :
            errors['name'] = "Name should be at least 3 characters"
        if len(formInfo['username']) < 3:
            errors['username'] = "Username should be at least 3 character"
        if not username_REGEX.match(formInfo['username']):           
            errors['username'] = ("Invalid username!")
        else:
            if len(filterResult) > 0:
                errors['filterResult'] = "username is already taken. Please choose another username."
        if len(formInfo['password']) < 6:
            errors['password'] = "Password should be at least 6 character"
        if (formInfo['confirmpw']) != (formInfo['password']):
            errors['confirmpw'] = "Password should be matching"
        return errors

    def login_validator(self, formInfo):
        filterResult = User.objects.filter(username=formInfo['username'])
        errors = {}
        if len(formInfo['username']) < 1:
            errors['username'] = "Username should be at least 1 character"
        if len(filterResult) == 0:
            errors['filterusername'] = "That account doesn't exist. Enter a different account"
        else:
            filterResult = filterResult[0]
            if bcrypt.checkpw(formInfo['password'].encode(), filterResult.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['wrongPassword'] = "Password does not match"
        return errors

class Tripmanager(models.Manager):
    def trip_validator(self, formInfo):
        d = datetime.now()
        now = d.strftime("%Y-%m-%d")
        errors = {}
        if len(formInfo['destination']) < 1:
            errors['destination'] = "Destination field can't be EMPTY"
        if len(formInfo['plan']) < 1:
            errors['plan'] = "Description field can't be EMPTY"
        if formInfo['datefrom'] < now:
            errors['datefrom'] = "Date From can't be past"
        if formInfo['dateto'] < formInfo['datefrom']:
            errors['dateto'] = "Date To field can't be the Past"
        return errors
            


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="tripscreated", on_delete = models.CASCADE)
    tripmember = models.ManyToManyField(User, related_name="tripsjoined")
    objects = Tripmanager()



