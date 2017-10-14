from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h1>Szercsy Lávcsy</h1>")

def static(request):
    return render(request,'hello.html')

def templ_example(request):
    return render(request,'templ_example.html',context = {"Field":"<h1>Tündér szercsy</h1>"})
