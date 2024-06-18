from django.urls import path
from .views import (RecipeListView, RecipeDeleteView, RecipeDetailView,
                    RecipeSearchView, CreateRecipeView, CreateIngredientView)
from . import views as recipe_views
urlpatterns = [
    path('', recipe_views.HomeView, name='home'),
    path('search/', RecipeSearchView.as_view(), name='recipeSearch'),
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/create/', CreateRecipeView.as_view(), name='recipesCreate'),
    path('recipes/create/ingredients/<int:pk>', CreateIngredientView.as_view(), name='recipesCreateIngredient'),
    path('recipes/create/ingredients/<int:pk>/delete/', recipe_views.delete_ingredient, name='recipesDeleteIngredient'),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipesDetail'),
    path('recipes/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipesDelete'),
    path('favourites/', recipe_views.favorite_recipes_list, name='favourites'),
    path('categories/', recipe_views.category_list, name='categories'),
    path('categories/<slug:slug>/', recipe_views.category_detail, name='categoryDetail'),
    path('myRecipes/', recipe_views.user_recipes_list, name='myRecipes'),
    path('favourities/<int:pk>/', recipe_views.addFavoriteRecipe, name='editFavorite'),

]