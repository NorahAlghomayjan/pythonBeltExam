from django.db import models
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def validRegister(self,post):
        errors = {}
        #checking name & username:
        if len(post['name']) < 3:
            errors['name'] = "Name should be at least 2 characters"
            
        if len(post['username']) < 3:
            errors['username'] = "Username should be at least 2 characters"
        
        #checking password:
        if len(post['pw']) < 8:
            errors['pw'] = "Password should be at least 8 characters"
        if post['pw'] != post['pw2']:
            errors['pw_match'] = "Passwords don't match "

        return errors

    def validLogin(self,post):
        errors = {}
        #fetching for the username in db.
        user = User.objects.filter(username=post['username'])

        #checking user (if user=none -> error , if user exist -> else)
        if not(user):
            errors ['username'] = 'username is not correct'
        elif not(bcrypt.checkpw(post['pw'].encode(), user[0].password.encode())):
            errors ['pw'] = 'Not correct password'
            print('--'*50,'Finish Errors')
        return errors

class ItemManager(models.Manager):
    def validItem (self,post):
        errors = {}
        try:
            item_name = post['item_name'] 
            if(len(item_name) < 3):
                errors ['item_name'] = 'item name at least 3 characters'
        except:
            errors ['item_name'] = 'item name could not be empty'
        return errors



class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50,blank=False,null=False)
    date_hired = models.DateField(blank=True,null=True)
    objects = UserManager()
    # wishlist = 1 user could have multiple items = wishlist
    # items = 1 user could create multiple items 

class Item(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    added_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,related_name='item',on_delete=models.CASCADE)
    users = models.ManyToManyField(User,related_name='wishlist')
    objects = ItemManager()
    # wishlist = 1 items could be in multiple wishlist
    # user = 1 item could be created by 1 user only.

# class Wishlist(models.Moddel):
#     pass