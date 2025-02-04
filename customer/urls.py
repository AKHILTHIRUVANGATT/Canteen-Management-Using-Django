from django.urls import path

from customer import views


app_name = "customer"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('forgot/', views.forgot, name="forgot"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    path('signup/', views.signup, name="signup"),
    path('guest/', views.guest, name="guest"),

    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

    path('menu/', views.menu, name="menu"),
    path('menu/category/<int:id>/', views.menu_cat, name="menu_cat"),
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:id>/', views.cart_add, name="cart_add"),
    path('cart/update/<int:id>/', views.cart_update, name="cart_update"),
    path('cart/remove/<int:id>/', views.cart_remove, name="cart_remove"),

    path('orders/', views.orders, name="orders"),
    path('payment/<int:id>/', views.payment, name="payment"),
    path('payment/card/<int:id>/', views.payment_card, name="payment_card"),
    path('payment/hand/<int:id>/', views.payment_hand, name="payment_hand"),
    path('feedback/<int:id>/', views.feedback, name="feedback"),
    path('feedback/view/<int:id>/', views.feedback_view, name="feedback_view"),



]