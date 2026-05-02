from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order {self.id} by {self.user}"

    # Total del pedido (suma de subtotales)
    def get_total(self):
        return sum(item.get_subtotal() for item in self.orderproduct_set.all())


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.order} - {self.product}"

    # Subtotal por producto (precio × cantidad)
    def get_subtotal(self):
        return self.product.price * self.quantity
