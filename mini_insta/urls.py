from django.urls import path
from .views import *

urlpatterns = [
    #empty string to show all page
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/post/create/<int:pk>/', CreatePostView.as_view(), name='create_post_form'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile_form'), # new
    path('profile/post/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post_form'), # new
    path('profile/post/update/<int:pk>/', UpdatePostView.as_view(), name='update_post_form'), # new
    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name='show_followers'), # new
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name='show_following'), # new
    path('profile/<int:pk>/feed/', ShowFeedDetailView.as_view(), name='show_feed'), # new
    path('profile/<int:pk>/search/', SearchView.as_view(), name='search'), # new
    path('profile/<int:pk>/search/results/', SearchResultsView.as_view(), name='search_results'), # new
    ]