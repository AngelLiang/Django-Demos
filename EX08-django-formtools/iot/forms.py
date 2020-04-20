from django import forms

from .models import Category, Device, Attribute, Value


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ['name']


class AttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = ['name']


class ValueForm(forms.ModelForm):

    class Meta:
        model = Value
        fields = '__all__'
