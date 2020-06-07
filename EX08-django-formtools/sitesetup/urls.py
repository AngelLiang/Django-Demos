from django.contrib import admin
from django.conf.urls import url
from django.urls import path

from . import forms
from .wizardviews import SiteSetupWizard, FORMS


# site_setup_wizard = SiteSetupWizard.as_view(
#     FORMS,
#     # url_name='setup',
#     # done_step_name='finished'
# )

urlpatterns = [
    path('', SiteSetupWizard.as_view(FORMS,)),
    # url(r'^(?P<step>.+)/$', site_setup_wizard, name='setup'),
]
