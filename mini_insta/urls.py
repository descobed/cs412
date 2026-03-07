from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    #empty string to show all page
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), 
    path('profile/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/', PublicProfileDetailView.as_view(), name='show_profile_by_pk'),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/post/create/', CreatePostView.as_view(), name='create_post_form'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile_form'),
    path('profile/post/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post_form'), 
    path('profile/post/update/<int:pk>/', UpdatePostView.as_view(), name='update_post_form'), 
    path('profile/followers/', ShowFollowersDetailView.as_view(), name='show_followers'), 
    path('profile/following/', ShowFollowingDetailView.as_view(), name='show_following'), 
    path('profile/feed/', ShowFeedDetailView.as_view(), name='show_feed'), 
    path('profile/search/', SearchView.as_view(), name='search'), 
    path('profile/search/results/', SearchResultsView.as_view(), name='search_results'), 
    path('create_profile/', CreateProfileView.as_view(), name='create_profile_form'),
    #Auth views
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
    ]