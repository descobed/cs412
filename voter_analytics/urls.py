#diego Escobedo Ruiz

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VoterListView.as_view(), name='home'),
    path(r'voters', views.VoterListView.as_view(), name='voters_list'),
    path(r'voters/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs', views.GraphListView.as_view(), name='graphs'),
]