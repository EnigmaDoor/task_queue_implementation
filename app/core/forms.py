from django import forms
from .models import Task

class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
