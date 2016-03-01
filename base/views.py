from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



def home(request):
    return HttpResponse('hello world')


def pledge(request):
    pass
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

