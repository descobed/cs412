from django.shortcuts import render
import os
from django.conf import settings


from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse
from .forms import CreatePostForm
from .forms import UpdateProfileForm
from .forms import CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

import discogs_client


#new ---
from rest_framework import generics
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your views here.

d = discogs_client.Client('ExampleApplication/0.1')

class ShowAllProfiles(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'        # note that this is plural 

    def dispatch(self, request, *args, **kwargs):
        '''overrides the basic method / checks for auth'''

        if request.user.is_authenticated:
            print(f"ShowAllView.dispatch(): request.user = {request.user}")
        else:
            print("ShowAllView.dispatch(): request.user is not authenticated")

        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'        # note that this is singular

    def get_object(self):
        '''Return the logged in user's profile'''
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self) -> str:
        '''Return to login'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        '''Return the context data for the profile detail view, including the user's posts.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['posts'] = Post.objects.filter(profile=profile).order_by('-created_at')
        return context


class PublicProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'


class PostDetailView(DetailView):
    # new 
    # Single post's detailed view. All images
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

#new
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''Return updated prof'''
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        '''Go to this after success'''
        return reverse('show_profile')

    def get_login_url(self) -> str:
        '''Return to login'''
        return reverse('login')

#new
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_queryset(self):
        '''Make sure user is logged in'''
        return Post.objects.filter(profile__user=self.request.user)

    def get_success_url(self):
        '''Go to this after success'''
        return reverse('show_profile')

    def get_login_url(self) -> str:
        '''Return to login'''
        return reverse('login')
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_queryset(self):
        '''Make sure user is logged in'''
        return Post.objects.filter(profile__user=self.request.user)

    def get_success_url(self):
        '''Go to this after success'''
        return reverse('show_profile')

    def get_login_url(self) -> str:
        '''return to login'''
        return reverse('login')


class CreatePostView(LoginRequiredMixin,CreateView):
    # view for creating a new post
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_profile(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        '''Saves a new post to the database.'''

        # attach this post to the profile
        form.instance.profile = self.get_profile()  # set the FK

        # Save the post first
        sm = super().form_valid(form)
       
        user = self.request.user
        form.instance.user = user

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
        return reverse('show_profile')
    
    def get_context_data(self, **kwargs):
        '''Returns the dictionary of context variables '''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def get_login_url(self) -> str:
        '''return to login'''
        return reverse('login')

class ShowFollowersDetailView(LoginRequiredMixin,DetailView):
    # new 
    # Single profile's followers view. All followers
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self) -> str:
        '''Redirect to login'''
        return reverse('login')

class ShowFollowingDetailView(LoginRequiredMixin,DetailView):
    # new 
    # Single profile's following view. All following
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self) -> str:
        '''Redirect to login'''
        return reverse('login')

class ShowFeedDetailView(LoginRequiredMixin,DetailView):
    # new 
    # Single profile's feed view. All posts by followed profiles
    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self) -> str:
        '''Redirects to login'''
        return reverse('login')

class SearchView(LoginRequiredMixin,DetailView):
    #new
    #Uses a DetailView / I don't understand why we'd want a list view here since we care more for the user's primary key

    model = Profile
    template_name = 'mini_insta/search.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self) -> str:
        '''Redirect to login'''
        return reverse('login')

class SearchResultsView(LoginRequiredMixin, DetailView):
    #new
    #once again I don't see the use of a listview here? 
    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Returns the logged in user's profile.'''
        return Profile.objects.get(user=self.request.user)

    def get_profiles(self):
        '''Returns the list of profiles matching the search query.'''
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Profile.objects.none()
        return Profile.objects.filter(display_name__icontains=query)

    def get_posts(self):
        '''Returns the list of posts matching the search query.'''
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        '''return context data'''
        context = super().get_context_data(**kwargs)
        context['search_results'] = self.get_profiles()
        context['search_results_posts'] = self.get_posts()
        context['query'] = self.request.GET.get('q', '').strip()
        return context
    
    def get_login_url(self) -> str:
        '''Redirect to login'''
        return reverse('login')

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def form_valid(self, form):
        '''Saves a new profile to the database.'''
        user_form = UserCreationForm(self.request.POST)

        #auto log in
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        #profile and user are the same
        form.instance.user = user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''gets context data / override the default method'''
        context = super().get_context_data(**kwargs)
        #pass the django user creation form too
        context['user_creation_form'] = UserCreationForm()
        return context

    def get_success_url(self):
        '''Show_profile after success'''
        return reverse('show_profile')
    

#NEW
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .models import Todo
from .serializers import TodoSerializer

class TodoUpdate(generics.UpdateAPIView):
    '''API view for updating a todo'''
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_update(self, serializer):
        '''Checks that the todo being updated belongs to the logged in user'''
        if self.request.user == serializer.instance.profile.user:
            serializer.save()

class TodoDelete(generics.DestroyAPIView):
    '''API view for deleting a todo'''
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_destroy(self, instance):
        '''Checks that the todo being deleted belongs to the logged in user'''
        if self.request.user == instance.profile.user:
            instance.delete()

class TodoListCreateAPIView(generics.ListCreateAPIView):
    '''API view for listing and creating todos'''
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        '''Sets the profile to the logged in user'''
        serializer.save(profile=self.request.user.profile)


#This creates a new DJANGO user, not a profile, but I believe that is the desired output

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginView(APIView):
    def post(self, request):
        '''User login and auth with tokens'''
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            profile = Profile.objects.filter(user=user).first()
            profile_id = profile.pk 
            return Response({'token': token.key, 'profile_id': profile_id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class DevLoginAPIView(APIView):
    '''DEBUG-only login that creates/uses a test user and returns auth token.'''

    def post(self, request):
        if not settings.DEBUG:
            return Response({'error': 'Not available'}, status=status.HTTP_404_NOT_FOUND)

        username = os.getenv('MINI_INSTA_DEV_USERNAME', 'mini_insta_test')
        password = os.getenv('MINI_INSTA_DEV_PASSWORD', 'mini_insta_test_pass')

        UserModel = get_user_model()
        user, created = UserModel.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )

        if created or not user.has_usable_password():
            user.set_password(password)
            user.save()

        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'username': username,
                'display_name': 'MiniInsta Test User',
                'bio_text': 'Auto-created test profile for DEBUG mode.',
            },
        )

        if not profile.username:
            profile.username = username
            if not profile.display_name:
                profile.display_name = 'MiniInsta Test User'
            profile.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'profile_id': profile.pk,
                'debug_login': True,
            },
            status=status.HTTP_200_OK,
        )


#NEW for API (names all single)
#register
class RegisterAPIView(generics.ListCreateAPIView):
    '''API view for registering a new user'''
    queryset = Profile.objects.all()
    serializer_class = UserSerializer



#Profile 
class ProfileListAPIView(generics.ListCreateAPIView):
    '''API view: List'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view: detail'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileFeedAPIView(generics.ListAPIView):
    """API view for a given profile's feed"""
    queryset = Profile.objects.all()
    serializer_class = PostSerializer # showing posts
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """gonna set posts to only
           Uses the get_post_feed function from the model """
        feed = Profile.objects.get(pk=self.kwargs['pk']).get_post_feed()
        return feed

#post
class PostListAPIView(generics.ListCreateAPIView):
    '''API view: List '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        '''Attaches the logged-in user's profile to the new post'''
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view: detail'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

#photo
#comment
#like
#follow

