from django import forms
from .models import Recipe, Ingredient, RecipeIngredient
from django.forms import inlineformset_factory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'content', 'difficulty', 'portions', 'cooking_time',
                  'category']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
