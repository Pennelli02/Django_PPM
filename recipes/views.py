from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RecipeForm, IngredientForm, RecipeIngredientForm
from .models import Recipe, Category, Ingredient


# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/allRecipes.html'
    ordering = ['-date_posted']


def HomeView(request):
    mostLikedRecipes = Recipe.objects.annotate(likeCount=Count('likes')).order_by('-likes')[:4]
    recentRecipes = Recipe.objects.order_by('-date_posted')[:4]
    return render(request, 'recipes/home.html', {'mostLiked': mostLikedRecipes, 'recent': recentRecipes})


# dopo si implementa la ricerca e l'ordinamento personalizzato
class RecipeDetailView(DetailView):
    model = Recipe


def recipe_create_view(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_form = IngredientForm(request.POST)
        recipe_ingredient_form = RecipeIngredientForm(request.POST)

        if recipe_form.is_valid() and ingredient_form.is_valid() and recipe_ingredient_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient = ingredient_form.save()
            recipe_ingredient = recipe_ingredient_form.save(commit=False)
            recipe_ingredient.recipe = recipe
            recipe_ingredient.ingredient = ingredient
            recipe_ingredient.save()

            return redirect(recipe.get_absolute_url())
    else:
        recipe_form = RecipeForm()
        ingredient_form = IngredientForm()
        recipe_ingredient_form = RecipeIngredientForm()

    context = {
        'recipe_form': recipe_form,
        'ingredient_form': ingredient_form,
        'recipe_ingredient_form': recipe_ingredient_form,
    }
    return render(request, 'recipes/recipe_form.html', context)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredient_formset'] = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        else:
            data['ingredient_formset'] = RecipeIngredientFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/profile/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


# mostra le ricette preferite
@login_required
def favorite_recipes_list(request):
    user = request.user
    fav_recipes = user.likes.all()
    return render(request, 'recipes/likeRecipe.html', {'recipes': fav_recipes})

# funzione per aggiungere o rimuovere una ricetta dai preferiti
@login_required
def addFavoriteRecipe(request, id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.likes.filter(user=user).exists():
        recipe.likes.remove(user)
        messages.success(request, f'Recipe {recipe.title} has been removed from favorites')
    else:
        recipe.likes.add(user)
        messages.success(request, f'Recipe {recipe.title} has been added')
    return redirect(recipe.get_absolute_url())

@login_required
def user_recipes_list(request):
    return render(request, 'recipes/userRecipes.html', {'recipes': Recipe.objects.filter(author=request.user)})


# mostra tutte le categorie presenti
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'recipes/categories.html', {'categories': categories})


# mostra le ricette presenti in una categoria
def category_detail(request, pk):
    categories = get_object_or_404(Category, pk=pk)
    return render(request, 'recipes/RecipesForCategories.html', {"categories": categories})


# implementa la ricerca per categoria e titolo
class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_search.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(categories__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
