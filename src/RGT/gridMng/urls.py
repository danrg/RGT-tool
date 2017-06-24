from django.conf.urls import url

from composite.views import CompositeWizard
from wizard.views import GridWizard
from .wizard import GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm
from .composite import FirstStepForm, WhichGridsForm, RulesForm
from . import views

grid_wizard_forms = [GeneralsForm, AlternativesForm, ConcernsForm, WeightsForm, RatingsForm]

composite_wizard_forms = [FirstStepForm, WhichGridsForm, RulesForm]

urlpatterns = [
               url(r'^$', views.getShowGridPage),
               url(r'^update/$', views.ajaxUpdateGrid),
               url(r'^delete/$', views.ajaxDeleteGrid),
               url(r'^create/$', views.ajaxCreateGrid),
               url(r'^createPage/$', views.getCreateMyGridPage, name='grid_in_place'),
               url(r'^dendrogram/$', views.ajaxGenerateDendogram),
               url(r'^similarity/$', views.ajaxGenerateSimilarity),
               url(r'^show/$', views.ajaxGetGrid),
               url(r'^show/(?P<usid>[a-zA-Z0-9]{0,50})$', views.show_grid),
               url(r'^timeline/(?P<usid>[a-zA-Z0-9]{0,50})', views.timeline),
               url(r'^timeline_json/(?P<usid>[a-zA-Z0-9]{0,50})', views.timeline_json),
               url(r'^download/$', views.ajaxGetSaveSvgPage),
               url(r'^download/dendrogram/$', views.dendrogramTo),
               url(r'^download/image/$', views.ajaxConvertSvgTo),
               url(r'^download/grid/$', views.ajaxConvertGridTo),
               url(r'^create/wizard/$', GridWizard.as_view(grid_wizard_forms), name='grid_wizard'),
               url(r'^create/composite/$', CompositeWizard.as_view(composite_wizard_forms), name='grid_composite'),
               url(r'^result.png$', views.pca),
               url(r'^image/(?P<usid>[a-zA-Z0-9]{0,50})/(?P<date>[0-9]{4}[-][0-9]{2}[-][0-9]{2}).png',
                   views.show_image)
               ]
