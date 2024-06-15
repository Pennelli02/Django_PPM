from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RecipeForm, IngredientForm, IngredientFormSet
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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('RecipeListView')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredient_formset'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredient_formset'] = IngredientFormSet(queryset=Ingredient.objects.none())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.save()
                self.object.ingredients.add(ingredient)
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


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
