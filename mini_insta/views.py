from django.shortcuts import render

from .models import Post, Profile
from django.views.generic import ListView
from django.views.generic import DetailView

# Create your views here.

class ShowAllProfiles(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'        # note that this is plural 

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'        # note that this is singular


class PostDetailView(DetailView):
    # new 
    # Single post's detailed view. All images
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'