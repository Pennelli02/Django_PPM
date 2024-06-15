from django.urls import path
from .views import (RecipeListView, RecipeCreateView, RecipeDeleteView, RecipeUpdateView, RecipeDetailView,
                    RecipeSearchView)
from . import views as recipe_views
urlpatterns = [
    path('', recipe_views.HomeView, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipesDetail'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipesCreate'),
    path('recipes/<slug:slug>/edit/', RecipeUpdateView.as_view(), name='recipesEdit'),
    path('recipes/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipesDelete'),
    path('favourites/', recipe_views.favorite_recipes_list, name='favourites'),
    path('categories/', recipe_views.category_list, name='categories'),
    path('categories/<slug:slug>/', recipe_views.category_detail, name='categoryDetail'),
    path('search/', RecipeSearchView.as_view(), name='recipeSearch'),
]