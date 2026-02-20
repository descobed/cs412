from django.urls import path
from .views import CreatePostView, PostDetailView, ProfileDetailView, ShowAllProfiles 

urlpatterns = [
    #empty string to show all page
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/post/create/<int:pk>/', CreatePostView.as_view(), name='create_post_form'), # new
    ]