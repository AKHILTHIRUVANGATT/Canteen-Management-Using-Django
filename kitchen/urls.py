from django.urls import path

from kitchen import views


app_name = "kitchen"

urlpatterns = [
    path('', views.orders, name="orders"),
    path('prepared/<int:id>/', views.order_pre, name="order_pre"),
    path('view/<int:id>/', views.order_view, name="order_view"),
    path('items/', views.items, name="items"),
    path('items/enable/<int:id>/', views.items_enable, name="items_enable"),
    path('items/disable/<int:id>/', views.items_disable, name="items_disable"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),

]