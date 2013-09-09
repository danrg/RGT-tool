from django.conf.urls.defaults import patterns, url
from RGT.gridMng.wizard.views import GridWizard
from RGT.gridMng.wizard.forms import GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm
from RGT.gridMng.composite.views import CompositeWizard
from RGT.gridMng.composite.forms import FirstStepForm, WhichGridsForm, BlaStepForm
from RGT.gridMng.trial.forms import ContactForm1, ContactForm2
from RGT.gridMng.trial.views import ContactWizard

grid_wizard_forms = [GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm]

composite_wizard_forms = [FirstStepForm, WhichGridsForm, BlaStepForm]

urlpatterns = patterns('',
    url(r'^$', 'RGT.gridMng.views.getShowGridPage'),
    url(r'^update/$', 'RGT.gridMng.views.ajaxUpdateGrid'),
    url(r'^delete/$', 'RGT.gridMng.views.ajaxDeleteGrid'),
    url(r'^create/$', 'RGT.gridMng.views.ajaxCreateGrid'),
    url(r'^createPage/$', 'RGT.gridMng.views.getCreateMyGridPage'),
    url(r'^dendrogram/$', 'RGT.gridMng.views.ajaxGenerateDendogram'),
    url(r'^similarity/$', 'RGT.gridMng.views.ajaxGenerateSimilarity'),
    url(r'^show/$', 'RGT.gridMng.views.ajaxGetGrid'),
    url(r'^download/$', 'RGT.gridMng.views.ajaxGetSaveSvgPage'),
    url(r'^download/dendrogram/$', 'RGT.gridMng.views.dendrogramTo'),
    url(r'^download/image/$', 'RGT.gridMng.views.ajaxConvertSvgTo'),
    url(r'^download/grid/$', 'RGT.gridMng.views.ajaxConvertGridTo'),
    url(r'^create/wizard/$', GridWizard.as_view(grid_wizard_forms)),
    url(r'^create/composite/$', CompositeWizard.as_view(composite_wizard_forms)),
    url(r'^result.png$', 'RGT.gridMng.views.pca'),
    url(r'^trial', ContactWizard.as_view([ContactForm1, ContactForm2]))
)