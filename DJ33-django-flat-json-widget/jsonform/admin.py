from django.contrib import admin
from django import forms
from flat_json_widget.widgets import FlatJsonWidget

from .models import JsonDocument


class JsonDocumentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'content': FlatJsonWidget
        }


class JsonDocumentAdmin(admin.ModelAdmin):
    form = JsonDocumentForm


admin.site.register(JsonDocument, JsonDocumentAdmin)
