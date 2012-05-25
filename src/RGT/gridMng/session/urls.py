from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'RGT.gridMng.session.views.getMySessionsPage'),
    url(r'^create/$', 'RGT.gridMng.session.views.ajaxCreateSession'),
    url(r'^show/$', 'RGT.gridMng.session.views.ajaxGetMySessionContentPage'),
    url(r'^participate/$', 'RGT.gridMng.session.views.ajaxGetParticipatingSessionContentPage'),
    url(r'^join/$', 'RGT.gridMng.session.views.ajaxJoinSession'),
    url(r'^state/$', 'RGT.gridMng.session.views.ajaxChangeSessionState'),
    url(r'^respond/$', 'RGT.gridMng.session.views.ajaxRespond'),
    url(r'^response/$', 'RGT.gridMng.session.views.ajaxGetParticipatingSessionsContentGrids'),
    url(r'^results/$', 'RGT.gridMng.session.views.ajaxGetResults'),
    url(r'^participants/$', 'RGT.gridMng.session.views.ajaxGetParticipatingPage'),
    url(r'^dendrogram/$', 'RGT.gridMng.session.views.ajaxGenerateSessionDendrogram'),
    url(r'^sessionGrid/$', 'RGT.gridMng.session.views.ajaxGetSessionGrid'),
)