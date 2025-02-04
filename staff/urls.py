from django.urls import path

from staff import views


app_name = "staff"

urlpatterns = [
    path('', views.orders, name="orders"),
    path('served/<int:id>/', views.order_serv, name="order_serv"),
    path('view/<int:id>/', views.order_view, name="order_view"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),

]