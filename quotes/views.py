import time
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def home_page(request):
    template_name = 'quotes/home.html'
    
    context = {
        'current_time': time.ctime(),
    }
    
    return render(request, template_name, context)

def about(request):
    template_name = 'quotes/about.html'
    return render(request, template_name)

def show_all(request):
    template_name = 'quotes/show_all.html'
    return render(request, template_name)