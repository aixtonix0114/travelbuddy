from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    encryptedPassword = request.POST['password']
    hashedPassword = bcrypt.hashpw(encryptedPassword.encode(),bcrypt.gensalt()).decode()
    user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashedPassword)
    request.session['loggedIninfo'] = user.id
    return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        loggedInUser = User.objects.filter(username = request.POST['username'])
        loggedInUser = loggedInUser[0]
        request.session['loggedIninfo'] = loggedInUser.id
        return redirect('/travels')

def travels(request):
    loggedInUser = User.objects.get(id=request.session['loggedIninfo'])
    allplansbyMe = Trip.objects.filter(Q(creator=loggedInUser) | Q(tripmember=loggedInUser))
    othersplans = Trip.objects.exclude(Q(creator=loggedInUser) | Q(tripmember=loggedInUser))
    Trip.objects.filter(Q(creator=loggedInUser) | Q(tripmember=loggedInUser))
    context = {
        'loggedIninfo': User.objects.get(id = request.session['loggedIninfo']),
        'allplansbyMe': allplansbyMe,
        'othersplans': othersplans
    }
    return render(request, 'travels.html', context)

def addpage(request):
    return render(request, 'addplan.html')

def addplan(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add')
    else:
        loggedInUser = User.objects.get(id = request.session['loggedIninfo'])
        addplan = Trip.objects.create(destination=request.POST['destination'], startdate=request.POST['datefrom'], enddate=request.POST['dateto'], plan=request.POST['plan'], creator=loggedInUser)
        request.session['createdplan'] = addplan.id
        return redirect('/travels')

def destInfo(request, other_id):
    thistrip = Trip.objects.get(id=other_id)
    travelers = thistrip.tripmember.all()
    context = {
        'trip': Trip.objects.get(id=other_id),
        'travelers': travelers
    }
    return render(request, 'destInfo.html', context)

def jointrip(request, other_id):
    loggedInUser = User.objects.get(id=request.session['loggedIninfo'])
    trip = Trip.objects.get(id=other_id)
    trip.tripmember.add(loggedInUser)
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')
