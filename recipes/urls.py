from django.urls import path
from .views import (RecipeListView, RecipeDeleteView, RecipeUpdateView, RecipeDetailView,
                    RecipeSearchView)
from . import views as recipe_views
urlpatterns = [
    path('', recipe_views.HomeView, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/create/', recipe_views.recipe_create_view, name='recipesCreate'),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipesDetail'),
    path('recipes/<slug:slug>/edit/', RecipeUpdateView.as_view(), name='recipesEdit'),
    path('recipes/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipesDelete'),
    path('favourites/', recipe_views.favorite_recipes_list, name='favourites'),
    path('categories/', recipe_views.category_list, name='categories'),
    path('categories/<slug:slug>/', recipe_views.category_detail, name='categoryDetail'),
    path('search/', RecipeSearchView.as_view(), name='recipeSearch'),
    path('myRecipes/', recipe_views.user_recipes_list, name='myRecipes'),
]