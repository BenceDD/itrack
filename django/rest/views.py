from django.shortcuts import render

from django.http import HttpResponse

import json

# Create your views here.

def example(request):
	return HttpResponse(json.dumps([{"Szercsy" : "Lavcsy"},1,2,3,4]))
