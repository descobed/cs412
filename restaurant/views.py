#diego Escobeod Ruiz


import random
from django.shortcuts import render
import datetime
import random

# Create your views here.

#specials for a rotating item on the menu
specials = ["chilaquiles","Milanesa","Tepache","Menudo","Torta de jamon"]


def home(request):
    '''Home view/landing page'''    
    template_name = 'restaurant/main.html'  

    
    return render(request, template_name)

def order(request):
    '''Page for inputing the order'''
    template_name = 'restaurant/order.html'  
    
    #choose the special for the day
    context = {
                "Special_food" : random.choice(specials)
            }

    return render(request, template_name, context)

def confirmation(request):
    '''Shows the confirmation page after order is placed'''
    if request.POST:
    
        template_name = 'restaurant/confirmation.html'
        #select a radom cooking time
        cooking_time = random.randint(30,60)
        #gets the current time
        current_time = datetime.datetime.now()
        #Uses timedelta to change the current time into the estimated finish time
        modified_time = current_time + datetime.timedelta(minutes=cooking_time)

        #All to be added to context if it is in the post request
        protein_list = []
        cost = 0

        if "Barbacoa" in request.POST:
            protein_list.append("Barbacoa")
            cost += 7
        if "Al Pastor" in request.POST:
            protein_list.append("Al pastor")
            cost += 5
        if "Bistec" in request.POST:
            protein_list.append("Bistec")
            cost += 6
        if "Lengua" in request.POST:
            protein_list.append("Lengua")
            cost += 6
        if "Special_food" in request.POST:
            protein_list.append("Special!")
            cost += 10
        if "name" in request.POST:
            name = request.POST.get("name")
        if "phone" in request.POST:
            phone = request.POST.get("phone")
        if "email" in request.POST:
            email = request.POST.get("email")
        if "Instructions" in request.POST:
            instructions = request.POST.get("Instructions")
            
        context = {
            #only the modified time needs to be dissplayed
            "modified_time" : modified_time,   
            "protein_list" : protein_list,
            "cost" : cost,
            "special_instructions" : instructions,
            "name" : name,
            "phone" : phone,
            "email" : email
        }

    
    return render(request, template_name, context=context)