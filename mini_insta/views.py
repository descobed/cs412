from django.shortcuts import render


from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse
from .forms import CreatePostForm
from .forms import UpdateProfileForm

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

#new
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_success_url(self):
        '''Redirects to the profile page after updating.'''
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})

#new
class DeletePostView(DeleteView):
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_success_url(self):
        '''Redirects to the profile page after deleting a post.'''
        pk = self.object.profile.pk  # get the profile's pk from the post
        return reverse('show_profile', kwargs={'pk': pk})
    
class UpdatePostView(UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        '''Redirects to the profile page after updating.'''
        return self.object.profile.get_absolute_url()


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

        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)


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

class ShowFollowersDetailView(DetailView):
    # new 
    # Single profile's followers view. All followers
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    # new 
    # Single profile's following view. All following
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFeedDetailView(DetailView):
    # new 
    # Single profile's feed view. All posts by followed profiles
    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

class SearchView(ListView):
    #new
    #new homework asks to use search_results here but I don't understand why a not search at the moment
    model = Profile
    template_name = 'mini_insta/search.html'
    context_object_name = 'profile'

class SearchResultsView(ListView):
    #new
    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'profiles'

    def get_profiles(self):
        '''Returns the list of profiles matching the search query.'''
        query = self.request.GET.get('q')
        return Profile.objects.filter(display_name__icontains=query)
    
    def get_posts(self):
        '''Returns the list of posts matching the search query.'''
        query = self.request.GET.get('q')
        return Post.objects.filter(caption__icontains=query)




