from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home', 'Home'),
    ]

    INVENTORY_STATUS_CHOICES = [
        ('INSTOCK', 'In Stock'),
        ('LOWSTOCK', 'Low Stock'),
        ('OUTOFSTOCK', 'Out of Stock'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventoryStatus = models.CharField(max_length=20, choices=INVENTORY_STATUS_CHOICES)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    image = models.CharField(max_length=100)  # just the image filename

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"