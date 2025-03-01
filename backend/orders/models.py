from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    # Связь с пользователем
    user = models.ForeignKey("authentaction.User", on_delete=models.CASCADE)
    
    # Связь с продуктом
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    # Сумма заказа (цена продукта)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Используем Decimal для точности

    # Статус заказа (оплачено/доставлено)
    status = models.CharField(
        max_length=20,
        choices=[('paid', 'Оплачено'), ('delivered', 'Доставлено')],
        default='paid',  # По умолчанию статус "оплачено"
    )

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username} на {self.product.title}"
