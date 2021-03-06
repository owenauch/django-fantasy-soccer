from django.conf.urls import url
from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^players/$', views.PlayerList.as_view()),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetail.as_view()),
    url(r'^rosters/$', views.RosterList.as_view()),
    url(r'^roster/(?P<pk>[0-9]+)/$', views.RosterDetail.as_view()),
    url(r'^matchweeks/$', views.MatchweekList.as_view()),
    url(r'^matchweek/(?P<pk>[0-9]+)/$', views.MatchweekDetail.as_view()),
    path('matchweek/<int:matchweek_pk>/scored-rosters/', views.ScoredRostersList.as_view()),
    path('matchweek/<int:matchweek_pk>/scored-rosters/<int:roster_pk>/', views.ScoredRostersDetail.as_view()),
    path('scored-rosters/', views.ScoredRostersAll.as_view()),
    url(r'^update-match-stats/(?P<date>\d{4}-\d{2}-\d{2})/$', views.UpdateMatchStats.as_view()),
    path('update-players/', views.UpdatePlayerStats.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)