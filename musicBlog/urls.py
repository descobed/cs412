from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'musicBlog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/add-friend/', AddFriendView.as_view(), name='add_friend'),
    path('profile/remove-friend/', RemoveFriendView.as_view(), name='remove_friend'),
    path('profile/friends/find/', FindFriendsView.as_view(), name='find_friends'),
    path('profile/friends/<int:pk>/', FriendProfileDetailView.as_view(), name='friend_profile'),
    path('discogs/search/', DiscogsSearchView.as_view(), name='discogs_search'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('artist/<int:pk>/', ArtistDetailView.as_view(), name='artist_detail'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:album_pk>/review/create/', CreateReviewView.as_view(), name='create_review'),
    path('discogs/save-and-view-artist/', SaveAndViewArtistView.as_view(), name='save_and_view_artist'),
    path('discogs/save-and-view-album/', SaveAndViewAlbumView.as_view(), name='save_and_view_album'),
    path('discogs/save-and-review/', SaveAndReviewView.as_view(), name='save_and_review'),
    path('login/', auth_views.LoginView.as_view(template_name='musicBlog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='musicBlog:home'), name='logout'),
]