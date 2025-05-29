from django.db import models
from django.conf import settings

from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  
    
    def __str__(self):
        return f"Cart for {self.user.email} - {self.created_at}"

    def get_total_cart_price(self):
        total_price = sum(item.get_total_items_price() for item in self.cart_items.all())
        return total_price

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Total: {self.get_total_items_price()}"

    def get_total_items_price(self):
        return self.product.price * self.quantity