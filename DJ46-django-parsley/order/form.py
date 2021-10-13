from django import forms
from parsley.decorators import parsleyfy
from .models import Order, Customer


@parsleyfy
class OrderForm(forms.ModelForm):
    title = forms.CharField(min_length=3, max_length=30)

    customer = forms.ModelChoiceField(
        label='客户', queryset=Customer.objects.all(), required=True,
    )

    class Meta:
        model = Order
        fields = '__all__'
        # parsley_extras = {
        #     'title': {
        #         'minlength': "5",
        #     },
        # }

    class Media:
        js = (
            "//code.jquery.com/jquery-latest.min.js",
            "parsley/js/parsley.min.js",
            "parsley/js/parsley.django-admin.js"
        )
