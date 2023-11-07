from django import forms
from .models import Tasks


class createTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "important"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Titulo",
            "description": "Descripción",
            "important": "Importante",
        }
