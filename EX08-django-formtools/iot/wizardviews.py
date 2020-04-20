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
from formtools.wizard.views import SessionWizardView

from . import forms

FORMS = [
    ("category", forms.CategoryForm),
    ("device", forms.DeviceForm),
    ("attribute", forms.AttributeForm),
    ("value", forms.ValueForm)
]


class DeviceWizard(SessionWizardView):
    """
    Some of these methods take an argument step, which is a zero-based counter
    as string representing the current step of the wizard.
    (E.g., the first form is '0' and the second form is '1')
    """

    def done(self, form_list, **kwargs):
        """override"""
        print(form_list)
        """print
        odict_values([<CategoryForm bound=True, valid=True, fields=(name)>, <DeviceForm bound=True, valid=True, fields=(name;category)>])
        """

        return HttpResponseRedirect(f'/admin/iot/device/')
        # return render(self.request, 'done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

    def get_form_step_data(self, form):
        """override"""
        return form.data

    def process_step(self, form):
        """override
        Hook for modifying the wizard’s internal state, given a fully validated Form object. The Form is guaranteed to have clean, valid data.

        This method gives you a way to post-process the form data before the data gets stored within the storage backend. By default it just returns the form.data dictionary. You should not manipulate the data here but you can use it to do some extra work if needed (e.g. set storage extra data).

        Note that this method is called every time a page is rendered for all submitted steps.
        """
        data = self.get_form_step_data(form)
        print(data)
        return data
