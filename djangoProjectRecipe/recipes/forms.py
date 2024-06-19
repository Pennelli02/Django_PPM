from django import forms
from .models import Recipe, Ingredient



class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'content', 'difficulty', 'portions', 'cooking_time',
                  'category']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']
