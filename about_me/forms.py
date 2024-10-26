from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'steps', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'maxlength': 100}),
        }
