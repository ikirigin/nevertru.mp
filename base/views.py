from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.



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
        d = {'name':name, 'email':email, 'party':party}
        return HttpResponse('POST /pledge dict:', str(d))
    return render_to_response('pledge.html', {})
    # load in the pledge form
    # take in a post from the pledge form


def verify(request, code):
    pass
    # load the verify + pledge form
    # if verified, load home page with message?
    # take a POST on the verify form


def verified(request):
    pass
    # the user is verified
    # load just the share tools

