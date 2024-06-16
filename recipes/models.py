from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from PIL import Image
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

# vengono create dall'amministratore (admin) l'utente le sceglie
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.name}"

    class Meta:
        app_label = 'recipes'


def generate_unique_slug(title):
    slug = slugify(title)
    unique_slug = slug
    counter = 1
    while Recipe.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug


class Recipe(models.Model):
    DIFFICULTY_LEVELS = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    ]
    image = models.ImageField(default='default.jpg', upload_to='recipesPics')
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS, default=3)
    portions = models.IntegerField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = ManyToManyField(Category)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.title)
        super().save(*args, **kwargs)

        self.resize_image()

    def resize_image(self):
        image = Image.open(self.image)
        img = Image.open(self.image.path)
        # metodo che serve a risparmiare spazio perché ridimensiona le immagini
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
