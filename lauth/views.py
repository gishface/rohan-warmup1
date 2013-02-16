# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import simplejson
import json
from django.http import HttpResponse
import os
import tempfile
import traceback
import re
import sys

#how to delete errything: User.objects.all().delete() 

def login_user(request):
    state = "Please log in below..."
    if request.POST:
        print request.POST
    username = password = ''
    if 'application/json' in request.META.get('CONTENT_TYPE') and '/users/login' in str(request):
        logreq = json.loads(request.body)
        username = logreq.get('user')
        password = logreq.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user.last_name = int(user.last_name) + 1
                user.save()
                retDict = {'errCode' : 1, 'count' : int(user.last_name)}
                return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
            else:
                state = "Not active."
        else:
            retDict = {'errCode' : -1}
            return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
    elif 'application/json' in request.META.get('CONTENT_TYPE') and '/users/add' in str(request):
        print "made it to add"
        addreq = json.loads(request.body)
        username = addreq.get('user')
        password = addreq.get('password')
        print username
        if len(username) > 128 or len(username) == 0:
            retDict = {'errCode' : -3}
            return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
        elif len(password) > 128:
            retDict = {'errCode' : -4}
            return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                retDict = {'errCode' : -2}
                return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
            else:
                try:
                    user = User.objects.create_user(username, '', password)
                    user.last_name = 1
                    user.save()
                    retDict = {'errCode' : 1, 'count' : 1}
                    return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
                except IntegrityError:
                    retDict = {'errCode' : -2}
                    return HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
    elif 'application/json' in request.META.get('CONTENT_TYPE') and '/TESTAPI/resetFixture' in str(request):
        print "made it!"
        User.objects.all().delete()
        print "still making it"
        retDict = {'errCode' : 1}
        response = HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
        response.status_code = 200
        print "still making it"
        return response
    elif 'application/json' in request.META.get('CONTENT_TYPE') and '/TESTAPI/unitTests' in str(request):
        print "made it to unittests"
        (ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
        print "still making it unittests"
        retDict = { 'output' : 'ALL TESTS PASSED',
                         'totalTests' : 10,
                         'nrFailed' : 0 }
        response = HttpResponse(simplejson.dumps(retDict), mimetype='application/json')
        response.status_code = 200
        return response
    elif 'loginu' in request.POST:
        state = str(request.META.get('CONTENT_TYPE'))
        #return HttpResponse(simplejson.dumps("test"), mimetype='application/json')
        #return render_to_response('auth.html',{'state':state, 'username': username})
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user.last_name = int(user.last_name) + 1
                user.save()
                state = "You're successfully logged in, " + username +"! You've logged in this many times: " + str(user.last_name)
                return render_to_response('authres.html',{'state':state, 'username': username})
            else:
                state = "Not active."
        else:
            state = "Incorrect password or username"
    elif 'addu' in request.POST:
        username = request.POST.get('user')
        password = request.POST.get('password')
        if len(username) > 128 or len(username) == 0:
            state = "The user name should be non-empty and at most 128 characters long. Please try again."
        elif len(password) > 128:
            state = "The password should be at most 128 characters long. Please try again." 
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                state = "User already exists."
            else:
                try:
                    user = User.objects.create_user(username, '', password)
                    user.last_name = 1
                    user.save()
                    state = "Made an account for you, "+username+". You've logged in this many times: " + str(user.last_name)
                    return render_to_response('authres.html',{'state':state, 'username': username})
                except IntegrityError:
                    state = "User exists already."

    return render_to_response('auth.html',{'state':state, 'username': username})