from django.db import models
from django.conf import settings


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ProductPhotos(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    photo = models.TextField()  # Фото хранится как строка base64

    def __str__(self):
        return f"Photo for product {self.product.id}"
