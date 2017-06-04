# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip

def index(request):
    return render(request, 'travel_buddy_app/index.html')

def login(request):
    if request.method == "POST":
        credentials = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
        print 'Checking credentials'
        valid = User.objects.login(credentials)
        if valid[0]:
            user = User.objects.get(username=request.POST['username'])
            print 'credentials verified'
            request.session['name'] = user.name
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            print 'HERE IS YOUR ID', user.id
            return redirect('/travels')
        else:
            print 'Somethings wrong'
            # create error messages
            messages.error(request, valid[1], extra_tags=valid[2])
            return redirect('/')
    return redirect('/')

def register(request):
    if request.method == "POST":
        print "-"*100
        registration = {
            'name' : request.POST['name'],
            'username' : request.POST['username'],
            'password' : request.POST['password'],
            'c_password' : request.POST['c_password'],
        }
        validation = User.objects.validate(registration)
        print validation
        if len(validation) < 4:
            del registration['c_password']
            User.objects.create(**registration)
            user = User.objects.get(username=request.POST['username'])
            print 'HERE IS YOUR ID', user.id
            print "User created"
            request.session['name'] = user.name
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            print "variables assigned to session"
            return redirect('/travels')
        else:
            print 'FAILED'
            # for each in validation:
            #     # messages.error(request, each[1], extra_tags=each[2])
            return redirect('/')
    return redirect('/')

def travels(request):
    this_user = User.objects.get(id=request.session['user_id'])
    trips = Trip.objects.exclude(users=this_user)
    user_trips = this_user.trips.all()
    context = {
    'user': request.session['name'],
    'trips': trips,
    'user_trips': user_trips
    }
    return render(request, 'travel_buddy_app/travels.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    return render(request, 'travel_buddy_app/add.html')

def process(request):
    if request.method == "POST":
        print "-"*100
        trip = {
            'destination' : request.POST['destination'],
            'plan' : request.POST['plan'],
            'start_date' : request.POST['start_date'],
            'end_date' : request.POST['end_date'],
        }
        print trip
        validation = Trip.objects.validateTrip(trip)
        print validation
        if len(validation) < 4:
            print trip
            this_trip = Trip.objects.create(**trip)
            print 'TRIP CREATED'
            this_user = User.objects.get(id= request.session['user_id'])
            this_user.trips.add(this_trip)
            print this_trip.users.all
            return redirect('/travels')
        else:
            for each in validation:
                messages.error(request, each[1], extra_tags=each[2])
            return redirect('/')
    return redirect('/')

def join(request, id):
    this_trip = Trip.objects.get(id= id)
    this_user = User.objects.get(id= request.session['user_id'])
    this_user.trips.add(this_trip)
    print 'USER ADDED'
    return redirect('/travels')

def trip(request, id):
    this_trip = Trip.objects.get(id= id)
    this_user = User.objects.get(id= request.session['user_id'])

    context = {
    'trip' : this_trip
    }
    return render(request, 'travel_buddy_app/trip.html', context)
