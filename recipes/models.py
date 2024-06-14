from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = ManyToManyField(Category)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        image = Image.open(self.image)
        img = Image.open(self.image.path)
        # metodo che serve a risparmiare spazio perché ridimensiona le immagini
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10)
    recipe = models.ManyToManyField(Recipe, related_name='ingredients')

    def __str__(self):
        return f"{self.quantity} of {self.name}"
