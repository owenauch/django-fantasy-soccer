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
    path('matchweek/<int:matchweek_pk>/scored_rosters', views.ScoredRostersList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)