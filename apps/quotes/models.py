from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from django.db.models import Count

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not postData['first_name'] or not postData['last_name'] or not postData['email'] or not postData['password'] or not postData['confirm']:
            errors['field'] = 'Field(s) must not be left empty.'
            return errors
        if not postData['first_name'].isalpha():
            errors['first_name'] = 'First name contains non-alpha characters.'
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name should be at least 3 characters.'
        if len(postData['first_name']) >= 255:
            errors['first_name'] = 'First name exceeds 255 character limit.'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last name should be at least 3 characters.'
        if len(postData['last_name']) >= 255:
            errors['last_name'] = 'Last name exceeds 255 character limit.'
        if not postData['last_name'].isalpha():
            errors['last_name'] = 'Last name contains non-alpha characters.'
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = 'Email is not valid.'
        if len(postData['email']) >= 255:
            errors['email'] = 'Email exceeds 255 character limit.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        if len(postData['password']) >= 16:
            errors['password'] = 'Password should not be more than 16 characters.'
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords do not match.'
        if User.objects.filter(email = postData['email']):
            errors['email'] = 'Username already exists.'
        return errors
    
    def infoValidator(self, postData):
        errors = {}
        if not postData['first_name'] or not postData['last_name'] or not postData['email']:
            errors['first_name'] = 'Field(s) must not be left empty.'
            return errors
        if not postData['first_name'].isalpha():
            errors['first_name'] = 'First name contains non-alpha characters.'
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name should be at least 3 characters.'
        if len(postData['first_name']) >= 255:
            errors['first_name'] = 'First name exceeds 255 character limit.'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last name should be at least 3 characters.'
        if not postData['last_name'].isalpha():
            errors['last_name'] = 'Last name contains non-alpha characters.'
        if len(postData['last_name']) >= 255:
            errors['last_name'] = 'Last name exceeds 255 character limit.'
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = 'Email is not valid.'
        if User.objects.filter(email = postData['email']):
            errors['email'] = 'Email already exists.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

    def __repr__(self):
        return "<User: {}|{} {} {} {}>".format(self.id, self.first_name, self.last_name, self.email, self.password)

class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}
        if not postData['quote'] or not postData['author']:
            errors['quote'] = 'Field(s) must not be empty.'
            return errors
        if len(postData['quote']) < 10:
            errors['quote'] = 'Quote must be more than 10 characters.'
        if len(postData['quote']) >= 255:
            errors['quote'] = 'Quote exceeds max limit of 255 characters.'
        if len(postData['author']) < 3:
            errors['author'] = 'Author must be more than 3 characters.'
        if len(postData['author']) >= 255:
            errors['author'] = 'Author exceeds max limit of 255 characters.'
        return errors

    def process_like(self, postData):
        this_user = User.objects.get(id = postData['user_id'])
        this_quote = Quote.objects.get(id = postData['quote_id'])
        this_quote.liked_users.add(this_user)
        liked_users = Quote.objects.annotate(count_likes=Count('liked_users'))
        return liked_users
    

class Quote(models.Model):
    quote = models.TextField(max_length=1000)
    author = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now= True)
    uploader = models.ForeignKey(User, related_name='uploaded_quotes')
    liked_users = models.ManyToManyField(User, related_name='liked_quotes')
    objects = QuoteManager()
    def __repr__(self):
        return "<Quote: {}|{}>".format(self.id, self.quote)