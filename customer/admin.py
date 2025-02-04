from django.contrib import admin

from .models import Customer, OrderItem, Order, Feedback, Payment

admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Feedback)
