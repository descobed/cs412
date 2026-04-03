from django.views import generic
from rest_framework import generics
from .serializers import *
from .models import * 
from django.views.generic import ListView, DetailView, UpdateView
import random

# Create your views here.

#had a home class but its the same as random

class random_joke(generic.TemplateView):
    '''View for showing a random joke and picture'''
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = Joke.objects.order_by('?').first()
        context['picture'] = Picture.objects.order_by('?').first()
        return context   
class random_picture(DetailView):
    '''View for showing a random picture'''
    model = Picture
    template_name = 'dadjokes/random_picture.html'
    context_object_name = 'picture'

    def get_object(self):
        '''Return a random picture'''
        return Picture.objects.order_by('?').first()

class JokeListView(ListView):
    '''View for listing all jokes'''
    model = Joke
    template_name = 'dadjokes/all_jokes.html'
    context_object_name = 'jokes'
class PictureListView(ListView):
    '''View for listing all pictures'''
    model = Picture
    template_name = 'dadjokes/all_pictures.html'
    context_object_name = 'pictures'

#detail views
class JokeDetailView(DetailView):
    '''View for showing a joke's details'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'
    def get_object(self):
        '''Return the joke with the given id'''
        return Joke.objects.get(id=self.kwargs['pk']) 
class PictureDetailView(DetailView):
    '''View for showing a picture's details'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'
    def get_object(self):
        '''Return the picture with the given id'''
        return Picture.objects.get(id=self.kwargs['pk'])    

#Jokes
class JokeListAPIView(generics.ListCreateAPIView):
    '''API view for listing and creating jokes'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view for retrieving, updating, and deleting a joke'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

#Pictures
class PictureListAPIView(generics.ListCreateAPIView):
    '''API view for listing and creating pictures'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view for retrieving, updating, and deleting a picture'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

#RANDOM views, uses retrieve since its only one object
class random_jokeAPIView(generics.RetrieveAPIView):
    '''API view for returning a random joke'''
    serializer_class = JokeSerializer
    def get_object(self):
        return Joke.objects.order_by('?').first()
class random_pictureAPIView(generics.RetrieveAPIView):
    '''API view for returning a random picture'''
    serializer_class = PictureSerializer
    def get_object(self):
        return Picture.objects.order_by('?').first()