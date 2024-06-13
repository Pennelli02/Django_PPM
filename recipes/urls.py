from django.urls import path
from .views import RecipeListView, RecipeCreateView, RecipeDeleteView, RecipeUpdateView, RecipeDetailView

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipesDetail'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipesCreate'),
    path('recipes/<slug:slug>/edit/', RecipeUpdateView.as_view(), name='recipesEdit'),
    path('recipes/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipesDelete'),

]