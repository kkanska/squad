from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.MatchesList.as_view(), name='matches_list'),
    path('new_matches_list/', views.NewMatchesList.as_view(), name='new_matches_list'),
    path('matches/<int:pk>/', views.MatchDetails.as_view()),
    path('generator/', views.GenerateRandomMatchesView.as_view(), name='generate'),
    path('invites/', views.InvitesList.as_view()),
    path('clear_db/', views.clear_db, name='clear_db')
]