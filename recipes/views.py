from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RecipeForm, IngredientForm
from .models import Recipe, Category, Ingredient


# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/allRecipes.html'
    ordering = ['-date_posted']


def HomeView(request):
    mostLikedRecipes = Recipe.objects.annotate(likeCount=Count('likes')).order_by('-likeCount')[:4]
    recentRecipes = Recipe.objects.order_by('-date_posted')[:4]
    return render(request, 'recipes/home.html', {'mostLiked': mostLikedRecipes, 'recent': recentRecipes})


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('recipesCreateIngredient', kwargs={'pk': self.object.pk})


class CreateIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipes/addIngredients.html'

    def dispatch(self, *args, **kwargs):  # per ulteriore controllo  verifica se esiste una ricetta con il pk fornito
        # e se l'utente corrente è l'autore di quella ricetta.
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        if self.recipe.author != self.request.user:
            messages.error(self.request, 'You do not have permission to add ingredients.')
            return redirect('home')  # Redirect to some error page or login page
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):  # Passa la ricetta al contesto del template in modo che possa essere
        # utilizzata nel rendering del template.
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        context['ingredients'] = Ingredient.objects.filter(recipe=self.recipe)
        return context

    def form_valid(self, form):  # Associa l'istanza della ricetta corrente al form dell'ingrediente prima di salvare.
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):  # Determina l'URL di successo in base al pulsante premuto dall'utente
        # (aggiungi un altro ingrediente o termina)
        if 'finish' in self.request.POST:
            messages.success(self.request, 'Your recipe has been successfully saved.')
            return reverse_lazy('recipesDetail', kwargs={'slug': self.recipe.slug})

        else:
            messages.success(self.request, 'Your ingredient has been successfully added.')
            return reverse_lazy('recipesCreateIngredient', kwargs={'pk': self.recipe.pk})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detailRecipe.html'
    context_object_name = 'recipe'
    slug_field = 'slug'  # Nome del campo nel modello
    slug_url_kwarg = 'slug'  # Nome del parametro nella URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.filter(recipe=self.object)
        return context


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
def addFavoriteRecipe(request, pk, slug):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk, slug=slug)
    if recipe.likes.filter(pk=user.pk).exists():
        recipe.likes.remove(user)
        messages.success(request, f'Recipe {recipe.title} has been removed from favorites')
    else:
        recipe.likes.add(user)
        messages.success(request, f'Recipe {recipe.title} has been added to favorites')
    return render(request, 'recipes/detailRecipe.html', {'recipe': recipe})


@login_required
def user_recipes_list(request):
    return render(request, 'recipes/userRecipes.html', {'recipes': Recipe.objects.filter(author=request.user)})


# mostra tutte le categorie presenti
def category_list(request, ):
    categories = Category.objects.all()
    return render(request, 'recipes/categories.html', {'categories': categories})


# mostra le ricette presenti in una categoria
def category_detail(request, slug):
    categories = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=categories)
    return render(request, 'recipes/RecipesForCategories.html', {"categories": categories, "recipes": recipes})


# implementa la ricerca per titolo
class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_search.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


# elimina gli ingredienti
@login_required
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    recipe = ingredient.recipe

    if recipe.author != request.user:
        messages.error(request, 'You do not have permission to delete this ingredient.')
        return redirect('home')  # Reindirizza a una pagina appropriata

    ingredient.delete()
    messages.success(request, 'Ingredient has been successfully deleted.')
    return redirect('recipesCreateIngredient', pk=recipe.pk)  # Reindirizza alla pagina di aggiornamento della
    # ricetta
