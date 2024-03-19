from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    @property
    def category_name(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.title

STARS = (
    (s, s * '*') for s in range(1,6)
)

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=1)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    @property
    def review(self):
        return self.text, self.stars 