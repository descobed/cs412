from django.urls import path
from .views import ProfileDetailView, ShowAllProfiles 

urlpatterns = [
    #empty string to show all page
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    ]