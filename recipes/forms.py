from django import forms
from .models import Recipe, Ingredient
from django.forms import modelformset_factory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'content', 'difficulty', 'portions', 'cooking_time',
                  'category']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']


# creo un form nel form che non dipenda dal foreign key
IngredientFormSet = modelformset_factory(Ingredient, form=IngredientForm, extra=1, can_delete=True)
