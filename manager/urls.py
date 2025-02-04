from django.urls import path

from manager import views


app_name = "manager"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),

    path('category/', views.category, name="category"),
    path('category/add/', views.category_add, name="category_add"),
    path('items/', views.items, name="items"),
    path('items/add/', views.items_add, name="items_add"),
    path('items/edit/<int:id>/', views.items_edit, name="items_edit"),
    path('items/enable/<int:id>/', views.items_enable, name="items_enable"),
    path('items/disable/<int:id>/', views.items_disable, name="items_disable"),
    path('offers/', views.offers, name="offers"),

    path('orders/', views.orders, name="orders"),
    path('payments/', views.payments, name="payments"),
    path('payments/complete/<int:id>/', views.payments_cmpt, name="payments_cmpt"),
    path('feedbacks/', views.feedbacks, name="feedbacks"),

    path('staffs/', views.staffs, name="staffs"),
    path('staffs/add/', views.staffs_add, name="staffs_add"),

    path('kitchens/', views.kitchens, name="kitchens"),
    path('kitchens/add/', views.kitchens_add, name="kitchens_add"),

    path('customers/', views.customers, name="customers"),

    path('analysis/customers', views.customers_by, name="customers_by"),
    path('analysis/orders/<int:id>/', views.order_customer, name="order_customer"),

    path('analysis/graph/', views.graph, name="graph"),

    path('analysis/orders/date/<int:id>/', views.order_date, name="order_date"),
    path('analysis/items/date/', views.items_date, name="items_date"),

    path('population-chart/', views.population_chart, name='population-chart'),


]