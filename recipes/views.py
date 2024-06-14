from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Recipe, Category


# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/home.html'

    def get_queryset(self):
        return Recipe.objects.annotate(num_likes=Count('likes')).order_by('-date_posted')


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['image', 'title', 'description', 'ingredients', 'price', 'content', 'difficulty', 'portions',
              'cooking-time', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['image', 'title', 'description', 'ingredients', 'price', 'content', 'difficulty', 'portions',
              'cooking-time', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


# mostra le ricette preferite
@login_required
def favorite_recipes_list(request):
    user = request.user
    recipes = Recipe.likes.filter(author=user)
    return render(request, 'recipes/likeRecipe.html', {'recipes': recipes})


# def user_recipes_list(request):
#    return render(request, 'recipes/userRecipes.html', {'recipes': Recipe.objects.filter(author=request.user)})

# mostra tutte le categorie presenti
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'recipes/categories.html', {'categories': categories})


# mostra le ricette presenti in una categoria
def category_detail(request, pk):
    categories = get_object_or_404(Category, pk=pk)
    return render(request, 'recipes/RecipesForCategories.html', {"categories": categories})
