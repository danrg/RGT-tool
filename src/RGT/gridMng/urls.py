from django.conf.urls import patterns, url
from RGT.gridMng.wizard.views import GridWizard
from RGT.gridMng.wizard.forms import GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm
from RGT.gridMng.composite.views import CompositeWizard
from RGT.gridMng.composite.forms import FirstStepForm, WhichGridsForm, RulesForm

grid_wizard_forms = [GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm]

composite_wizard_forms = [FirstStepForm, WhichGridsForm, RulesForm]

urlpatterns = patterns('',
    url(r'^$', 'RGT.gridMng.views.getShowGridPage'),
    url(r'^update/$', 'RGT.gridMng.views.ajaxUpdateGrid'),
    url(r'^delete/$', 'RGT.gridMng.views.ajaxDeleteGrid'),
    url(r'^create/$', 'RGT.gridMng.views.ajaxCreateGrid'),
    url(r'^createPage/$', 'RGT.gridMng.views.getCreateMyGridPage', name='grid_in_place'),
    url(r'^dendrogram/$', 'RGT.gridMng.views.ajaxGenerateDendogram'),
    url(r'^similarity/$', 'RGT.gridMng.views.ajaxGenerateSimilarity'),
    url(r'^show/$', 'RGT.gridMng.views.ajaxGetGrid'),
    url(r'^show/(?P<usid>[a-zA-Z0-9]{0,50})$', 'RGT.gridMng.views.show_grid'),
    url(r'^timeline/(?P<usid>[a-zA-Z0-9]{0,50})', 'RGT.gridMng.views.timeline'),
    url(r'^timeline_json/(?P<usid>[a-zA-Z0-9]{0,50})', 'RGT.gridMng.views.timeline_json'),
    url(r'^download/$', 'RGT.gridMng.views.ajaxGetSaveSvgPage'),
    url(r'^download/dendrogram/$', 'RGT.gridMng.views.dendrogramTo'),
    url(r'^download/image/$', 'RGT.gridMng.views.ajaxConvertSvgTo'),
    url(r'^download/grid/$', 'RGT.gridMng.views.ajaxConvertGridTo'),
    url(r'^create/wizard/$', GridWizard.as_view(grid_wizard_forms), name='grid_wizard'),
    url(r'^create/composite/$', CompositeWizard.as_view(composite_wizard_forms), name='grid_composite'),
    url(r'^result.png$', 'RGT.gridMng.views.pca'),
    url(r'^show/(?P<usid>[a-zA-Z0-9]{0,50}).png', 'RGT.gridMng.views.show_image')
)