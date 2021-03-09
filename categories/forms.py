from django import forms
from django.forms import ModelForm
from .models import Category

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'brief_description']
