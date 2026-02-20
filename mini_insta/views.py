from django.shortcuts import render


from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse
from .forms import CreatePostForm

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


class CreatePostView(CreateView):
    # new
    # view for creating a new post
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def form_valid(self, form):
        '''Saves a new post to the database.'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this post to the profile
        form.instance.profile = profile  # set the FK

        # Save the post first
        sm = super().form_valid(form)
        
        # Create Photo object if URL was provided
        image_url = form.cleaned_data.get('image_url')
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return sm
    
    def get_success_url(self):
        '''Redirects to the profile page after creating a post.'''
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        '''Returns the dictionary of context variables '''
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context