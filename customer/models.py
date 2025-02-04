from django.db import models

from manager.models import Menu
from user.models import User
from staff.models import Staff


class Customer(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = 'customer_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ('id',)

    def __str__(self):

        return self.name
    

class OrderItem(models.Model):
    created_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)
    amount = models.FloatField()


    class Meta:
        db_table = 'customer_order_cart'
        verbose_name = 'order cart'
        verbose_name_plural = 'order carts'
        ordering = ('id',)

    def __str__(self):

        return self.menu.name
    
    

class Order(models.Model):
    created_datetime = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    table = models.IntegerField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'is_active':True})
    items = models.ManyToManyField(OrderItem, related_name='items')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    is_pending = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_prepared = models.BooleanField(default=False)
    is_payement = models.BooleanField(default=False)
    is_feedback = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('id',)

    def __str__(self):

        return self.user.first_name
    

class Payment(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_done = models.BooleanField(default=False)


    class Meta:
        db_table = 'customer_payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ('id',)

    def __str__(self):

        return self.user.first_name
    

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()


    class Meta:
        db_table = 'customer_feedback'
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'
        ordering = ('id',)

    def __str__(self):

        return self.user.first_name