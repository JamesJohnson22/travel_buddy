# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):

    def validate(self, data):
        response = []
        errors = 0

        # check name
        if data['name'].isalpha() and len(data['name']) > 2:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Name must be all letters and at least 2 characters', 'name'])

        # check username
        if data['username'].isalpha() and len(data['username']) > 2:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Username must be all letters and at least 3 characters', 'username'])

        # check password
        if len(data['password']) > 7:
            if data['password'] == data['c_password']:
                response.append([True, '', ''])
            else:
                errors += 1
                response.append([False, 'Passwords must match', 'c_password'])
        else:
            errors += 1
            response.append([False, 'Password must be at least 8 characters', 'password'])

        # check for any errors and return approriate message if so, no errors then just return successful message
        if errors > 0:
            return response
        return [True, '', '']

    def validateTrip(self, data):
        response = []
        errors = 0

        # check destination
        if len(data['destination']) > 0:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Destination must not be empty!', 'destination'])

        # check plan
        if len(data['plan']) > 0:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Description must not be empty', 'description'])

        # check start_date
        if len(data['start_date']) > 0:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Start date must not be empty', 'start_date'])

        # check end_date
        if len(data['end_date']) > 0:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'End date must not be empty', 'end_date'])

        if errors > 0:
            return response
        return [True, '', '']

    def login(self, data):
        # first check if information entered is valid before we ping db
        if data['username'].isalpha() and len(data['username']) > 2:
            # if valid then check if credentials match those stored in db
            try:
                if self.get(username = data['username']):
                    if self.get(username = data['username']).password == data['password']:
                        return [True, '', '']
                    else:
                        return [False, 'Incorrect username or password', 'login-error']
            except:
                return [False, 'Incorrect username or password', 'login-error']
        # if info is not valid then just return error and not ping db
        else:
            return [False, 'Incorrect username or password', 'login-error']

class User(models.Model):
    name = models.CharField(max_length = 30, default='testname')
    username = models.CharField(max_length = 30, default='testusername')
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Trip(models.Model):
    users = models.ManyToManyField(User, related_name="trips")
    destination = models.CharField(max_length = 50, default='testdestination')
    plan = models.CharField(max_length = 255, default='testplan')
    start_date = models.CharField(max_length = 50)
    end_date = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
