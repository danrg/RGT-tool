from django.conf.urls import url
from . import views

urlpatterns = [
                       url(r'^$', views.getMySessionsPage),
                       url(r'^create/$', views.ajaxCreateSession),
                       url(r'^show/$', views.ajaxGetMySessionContentPage),
                       url(r'^show/(?P<usid>[a-zA-Z0-9]{0,50})$', views.show_detailed),
                       url(r'^participate/(?P<usid>[a-zA-Z0-9]{0,50})$', views.participate_detailed),
                       url(r'^join/(?P<key>[-a-f0-9]{36})$', views.join_session),
                       url(r'^latest/$', views.show_latest),
                       url(r'^participate/$', views.ajaxGetParticipatingSessionContentPage),
                       url(r'^join/$', views.ajaxJoinSession),
                       url(r'^state/$', views.ajaxChangeSessionState),
                       url(r'^respond/$', views.ajaxRespond),
                       url(r'^response/$', views.ajaxGetParticipatingSessionsContentGrids),
                       url(r'^results/$', views.ajaxGetResults),
                       url(r'^responseResults/$', views.ajaxGetResponseResults),
                       url(r'^participants/$', views.ajaxGetParticipatingPage),
                       url(r'^dendrogram/$', views.ajaxGenerateSessionDendrogram),
                       url(r'^sessionGrid/$', views.ajaxGetSessionGrid),
                       url(r'^download/results/$', views.ajaxDownloadSessionResults)
]