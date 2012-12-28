from django.conf.urls.defaults import patterns, url
from RGT.gridMng.wizard.views import GridWizard
from RGT.gridMng.wizard.forms import GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm

grid_wizard_forms = [GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm]

urlpatterns = patterns('',
    url(r'^$', 'RGT.gridMng.views.getShowGridPage'),
    url(r'^update/$', 'RGT.gridMng.views.ajaxUpdateGrid'),
    url(r'^delete/$', 'RGT.gridMng.views.ajaxDeleteGrid'),
    url(r'^create/$', 'RGT.gridMng.views.ajaxCreateGrid'),
    url(r'^dendrogram/$', 'RGT.gridMng.views.ajaxGenerateDendogram'),   
    url(r'^show/$', 'RGT.gridMng.views.ajaxGetGrid'),
    url(r'^download/$', 'RGT.gridMng.views.ajaxGetSaveSvgPage'),
    url(r'^download/dendrogram/$', 'RGT.gridMng.views.dendrogramTo'),
    url(r'^download/image/$', 'RGT.gridMng.views.ajaxConvertSvgTo'),
    url(r'^create/wizard/$', GridWizard.as_view(grid_wizard_forms)),
)