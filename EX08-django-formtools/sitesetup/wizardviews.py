"""

How it works

Here’s the basic workflow for how a user would use a wizard:

    1. The user visits the first page of the wizard, fills in the form and submits it.
    2. The server validates the data. If it’s invalid, the form is displayed again, with error messages. If it’s valid, the server saves the current state of the wizard in the backend and redirects to the next step.
    3. Step 1 and 2 repeat, for every subsequent form in the wizard.
    4. Once the user has submitted all the forms and all the data has been validated, the wizard processes the data – saving it to the database, sending an email, or whatever the application needs to do.

"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from formtools.wizard.views import SessionWizardView

from . import forms

FORMS = [
    ('welcome', forms.WalcomeForm),
    # ("create", forms.CreateSuperUserForm),
    ('create', forms.UserCreationForm),
]

TEMPLATES = {
    'welcome': 'sitesetup/welcome.html',
    'create': 'sitesetup/createsuperuser.html',
    'done': 'sitesetup/done.html',
    'exist': 'sitesetup/exist.html',
}


class SiteSetupWizard(SessionWizardView):
    """
    Some of these methods take an argument step, which is a zero-based counter
    as string representing the current step of the wizard.
    (E.g., the first form is '0' and the second form is '1')
    """

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """override"""
        # print(form_list)
        for form in form_list:
            form.save()

        template = TEMPLATES['done']
        return render(self.request, template, {
            'form_data': [form.cleaned_data for form in form_list],
        })

    def process_step(self, form):
        # print(self.steps.current)
        return self.get_form_step_data(form)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if 'create' == self.steps.current:
            superuser = User.objects.filter(is_superuser=True).all()
            print(superuser)
            if superuser:
                pass
        return context

    def render(self, form=None, **kwargs):
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)
