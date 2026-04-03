
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.random_joke.as_view(), name="home"),
    path(r'random/', views.random_joke.as_view(), name="random"),
    path(r'jokes/', views.JokeListView.as_view(), name="all_jokes"),
    path(r'joke/<int:pk>/', views.JokeDetailView.as_view(), name="joke"),
    path(r'pictures/', views.PictureListView.as_view(), name="all_pictures"),
    path(r'picture/<int:pk>/', views.PictureDetailView.as_view(), name="picture"),

    #API
    path(r'api/jokes/', views.JokeListAPIView.as_view()),
    path(r'api/random/', views.random_jokeAPIView.as_view()),
    path(r'api/joke/<int:pk>/', views.JokeDetailAPIView.as_view()),
    path(r'api/pictures/', views.PictureListAPIView.as_view()),
    path(r'api/picture/<int:pk>/', views.PictureDetailAPIView.as_view()),
    path(r'api/random_picture/', views.random_pictureAPIView.as_view()),
]
