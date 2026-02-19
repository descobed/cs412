from django.urls import path
from .views import PostDetailView, ProfileDetailView, ShowAllProfiles 

urlpatterns = [
    #empty string to show all page
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    ]