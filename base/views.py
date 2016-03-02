from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from base.models import Pledge
import random

"""
TODO

implement post pledge share page

implement verify page on same url as share page

implement verification + pledge process

implement signed in home page 

"""



def home(request):
    # if signed in
    # if have pledge, redirect to code
    # if no pledge, show pledge form
    user = request.user
    if user.is_authenticated():
        pledge = Pledge.get_user_pledge(user)
        if pledge: 
            if pledge.code:
                return HttpResponseRedirect('/{}'.format(pledge.code))
            else:
                return HttpResponse('missing pledge code')
                
            
    context = RequestContext({})
    return render_to_response('pledge.html', {}, context_instance=RequestContext(request))
    

def login_user(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


def reflect_user(request):
    return HttpResponse('user:',str(request.user))


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('home')+'?loggedout')


def makepledge(request):
    if request.method == 'GET':
        context = RequestContext({})
        return render_to_response('pledge.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(reverse('home')+'?already_pledged')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        party = request.POST.get('party','')
        party = request.POST.get('party','')
        verifycode = request.POST.get('verifycode','')
        if not name or not email or not party:
            return HttpResponseRedirect(reverse('home')+"?missing_field")
        if '@' not in email:
            return HttpResponseRedirect(reverse('home')+"?bad_email")
        if party not in ['Republican', 'Democrat', 'Other']:
            return HttpResponseRedirect(reverse('home')+"?bad_party")
        user, pledge = take_pledge(name, email, party)
        if not user:
            return HttpResponseRedirect(reverse('home')+"?bad_user")
        if not pledge:
            return HttpResponseRedirect(reverse('home')+"?bad_pledge")
        # sign in the user
        login_user(request, user)
        if verifycode:
            Pledge.verify(user, verifycode)
        return HttpResponseRedirect('/{}'.format(pledge.code))
        d = {'name':name, 'email':email, 'party':party}
        print(d)
        return HttpResponse('POST /pledge dict:', str(d))


def verifypledge(request, code):
    """
    if not valid code
        bounce
    if authed
        if theirs
          
        if not theirs
        
    if not authed
     
        if this is their code
            if it is verified
            
            if it is not verified
        if this code is invalid
        if this is not their code
            
    if user isn't signed in
        if the code is valid
    
    """
    pledge = Pledge.get_by_code(code)
    if not pledge:
        return HttpResponseRedirect(reverse('home')+"?bad_code") 
    
    if request.method == 'GET':
        pass
        # put in most of this stuff here
    elif request.method == 'POST':
        # take in the pledge params
        pass
    user = request.user
    is_authenticated = user.is_authenticated()
    is_verified = pledge.verified
    is_owned = is_authenticated and pledge.user == user
    context = {
        'user' : request.user,
        'pledge' : pledge, 
        'is_verified' : pledge.verified,
        'is_authenticated' : request.user.is_authenticated(),
        'is_owned' : pledge.user == request.user,
    }
    return render_to_response('confirm.html', context, context_instance=RequestContext(request))


def verify(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('home')+'?no_post_to_verify')
    verifycode = request.POST.get('verifycode', '')
    if not verifycode:
        return HttpResponseRedirect(reverse('home')+'?no_verifycode')
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('home')+'?not_authed')
    Pledge.verify(user, verifycode)
    return HttpResponseRedirect(reverse('home')+'?verified')
    

def take_pledge(name, email, party):
    user = get_or_create_user(name, email)
    pledge = Pledge.user_create(user, party)
    return user, pledge


def get_or_create_user(name, email):
    user = get_user(email)
    if not user:
        user = User.objects.create_user(email, email, gen_password(), first_name=name)
        user.save()
    return user


def gen_password(length=20):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(length))  


def get_user(email):
    try:
        user = User.objects.filter(email=email)[0]
    except:
        user = None
    return user

