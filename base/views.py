from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def home(request):
    context = RequestContext({})
    return render_to_response('pledge.html', {}, context_instance=RequestContext(request))
    

def pledge(request):
    if request.method == 'GET':
        return HttpResponse('GET pledge endpoint')
    elif request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        party = request.POST.get('party','')
        if not name or not email or not party:
            return HttpResponseRedirect(reverse('home')+"?missing_field")
        if party not in ['Republican', 'Democrat', 'Other']:
            return HttpResponseRedirect(reverse('home')+"?bad_party")
        user, pledge = take_pledge(name, email, party)
        d = {'name':name, 'email':email, 'party':party}
        print(d)
        return HttpResponse('POST /pledge dict:', str(d))
    return render_to_response('pledge.html', {})
    # load in the pledge form
    # take in a post from the pledge form


def take_pledge(name, email, party):
    user = get_or_create_user(name, email)
    pledge = Pledge.user_create(user, party)
    pass


def get_or_create_user(name, email):
    user = get_user(email)
    if not user:
        user = User.objects.create_user(name, email, gen_password())
    return user


def gen_password(length=16):
    return ''.join(choice(chars) for _ in range(length))  


def get_user(email):
    try:
        user = User.objects.filter(email=email)[0]
    except:
        user = None
    return user


def verify(request, code):
    pass
    # load the verify + pledge form
    # if verified, load home page with message?
    # take a POST on the verify form


def verified(request):
    pass
    # the user is verified
    # load just the share tools

