from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'RGT.gridMng.views.getShowGridPage'),
    url(r'^update/$', 'RGT.gridMng.views.ajaxUpdateGrid'),
    url(r'^delete/$', 'RGT.gridMng.views.ajaxDeleteGrid'),
    url(r'^create/$', 'RGT.gridMng.views.ajaxCreateGrid'),
    url(r'^dendrogram/$', 'RGT.gridMng.views.ajaxGenerateDendogram'),   
    url(r'^show/$', 'RGT.gridMng.views.ajaxGetGrid'),
    url(r'^download/$', 'RGT.gridMng.views.ajaxSaveSvgPage'),
    url(r'^download/image/$', 'RGT.gridMng.views.ajaxConvertSvgTo'),
)