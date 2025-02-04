import datetime
import random

from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_customer
from main.functions import generate_form_errors

from manager.models import Manager, Category, Menu
from customer.models import Customer, Order, Payment, Feedback, OrderItem
from kitchen.models import Kitchen
from staff.models import Staff
from manager.forms import CategoryForm, ItemForm, UserForm
from user.models import User


@login_required(login_url="/login")
def index(request):
    menus = Menu.objects.filter(is_active=True, is_featured=True)
    user= request.user

    conntext = {
        "title": "Canteen Management",
        "menus":menus,
        "user":user,
    }
    return render(request, 'customer/index.html', context=conntext)



def forgot(request):

    conntext = {
        "title": "Canteen Management",
    }
    return render(request, 'customer/forgot.html', context=conntext)



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("customer:index"))
            else:
                context= {
                    "title": "Customer | Login",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "customer/login.html", context=context)
        else:
            context= {
                "title": "Customer | Login",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "customer/login.html", context=context)
    else:
        context= {
            "title" : "Customer | Login"
        }
        return render(request, "customer/login.html", context=context)



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("customer:login"))



@login_required(login_url="/login")
def account(request):
    user=request.user
    customer= Customer.objects.get(user=user)

    if request.method == "POST":
        email=request.POST.get("email")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        user.email = email
        user.first_name = name
        user.mobile = mobile
        user.set_password(password)

        user.save()

        customer.name = name

        customer.save()

    context= {
        "title": "Customer | Account",
        "customer":customer,
        "user": user,
    }
    return render(request, "customer/account.html", context=context)



def signup(request):

    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        name = request.POST.get("name")
        mobile=request.POST.get("mobile")

        if not User.objects.filter(mobile=mobile).exists():

            if not User.objects.filter(email=email).exists():

                form = UserForm(request.POST,request.FILES)

                if form.is_valid():

                    user = User.objects.create_user(
                        username = username,
                        password = password,
                        email = email,
                        first_name = name,
                        mobile = mobile,
                        is_customer=True
                    )

                    customer = Customer.objects.create(
                        user=user,
                        name=user.first_name,
                    )
                    customer.save()

                    user.save()

                    return HttpResponseRedirect(reverse("customer:login"))
                else:
                    message = generate_form_errors(form)
                    form = UserForm()
                    context= {
                        "title": "Customer | Signup",
                        "error": True,
                        "message": message,
                        "form": form,
                    }
                    return render(request, "customer/signup.html", context=context)
                
            else:
                form = UserForm()
                context= {
                    "title": "Customer | Signup",
                    "error": True,
                    "message": "Email already used",
                    "form": form,
                }
                return render(request, "customer/signup.html", context=context)
        else:
            form = UserForm()
            context= {
                "title": "Customer | Signup",
                "error": True,
                "message": "Mobile already used",
                "form": form,
            }
            return render(request, "customer/signup.html", context=context)

    else:
        form = UserForm()
        context= {
            "title": "Customer | Signup",
            "form": form,
        }
        return render(request, "customer/signup.html", context=context)
    

def guest(request):

    number= random.randint(1000, 1000000)
    username=str(number)
    user = User.objects.create_user(
        username = username,
        password = "Password@123",
        email = "guest@example.com",
        first_name = "Guest",
        is_guest=True
    )
    user.save()

    guest = authenticate(request, username=username, password="Password@123")
    if guest is not None:
        auth_login(request, guest)

        return HttpResponseRedirect(reverse("customer:index"))

    return HttpResponseRedirect(reverse("customer:index"))


@login_required(login_url="/login")
def about(request):
    user= request.user

    context= {
        "title": "Canteen | About",
        "user": user
    }
    return render(request, "customer/about.html", context=context)


@login_required(login_url="/login")
def contact(request):

    user= request.user

    context= {
        "title": "Canteen | Contact",
        "user":user
    }
    return render(request, "customer/contact.html", context=context)


@login_required(login_url="/login")
def menu(request):

    menus = Menu.objects.filter(is_active=True)
    user= request.user
    categories= Category.objects.all()

    context= {
        "title": "Canteen | Menu",
        "menus":menus,
        "user":user,
        "categories":categories,
        "user":user
    }
    return render(request, "customer/menu.html", context=context)

@login_required(login_url="/login")
def menu_cat(request,id):
    cat= Category.objects.get(id=id)

    menus = Menu.objects.filter(is_active=True, category=cat)
    user= request.user
    categories= Category.objects.all()

    context= {
        "title": "Canteen | Menu",
        "menus":menus,
        "user":user,
        "categories":categories,
    }
    return render(request, "customer/menu.html", context=context)


@login_required(login_url="/login")
def cart(request):

    user= request.user
    name=user.first_name
    carts = OrderItem.objects.filter(user=user, ordered=False)
    total_amount = carts.aggregate(Sum("amount"))["amount__sum"]

    if request.method == "POST":
        table = request.POST.get("table")
        if table:
            instance= Order.objects.create(
                user=user,
                name=name,
                table=table,
                subtotal=total_amount,
                total=total_amount,
            )
            payment = Payment.objects.create(
                Order=instance,
                amount=instance.total,
                user=user,
            )
            payment.save()
            for cart in carts:
                instance.items.add(cart)
                cart.ordered=True
                cart.save()
            instance.save()

            return HttpResponseRedirect(reverse("customer:orders"))
        else:

            context= {
            "title": "Canteen | Menu",
                "error": True,
                "message": "message",
                "title": "Canteen | Menu",
                "carts":carts,
                "user":user,
                "total_amount":total_amount,
            }
            return render(request, "customer/cart.html", context=context)

    context= {
        "title": "Canteen | Menu",
        "carts":carts,
        "user":user,
        "total_amount":total_amount,

    }
    return render(request, "customer/cart.html", context=context)


@login_required(login_url="/login")
def cart_add(request, id):
    user=request.user
    menu = Menu.objects.get(id=id)
    if not user.is_customer:
        amount=menu.price
    else:
        amount=menu.offer_price

    cart = OrderItem.objects.create(
        user=user,
        menu=menu,
        amount=amount,
        qty=1,
        ordered=False,
    )
    cart.save()

    return HttpResponseRedirect(reverse("customer:cart"))


@login_required(login_url="/login")
def cart_update(request, id):
    user=request.user
    cart = OrderItem.objects.get(id=id)
    menu=cart.menu
    initial_amount=cart.amount

    if not user.is_customer:
        amount=menu.price + initial_amount
    else:
        amount=menu.offer_price + initial_amount


    cart.amount=amount
    cart.qty +=1
    cart.save()
        

    return HttpResponseRedirect(reverse("customer:cart"))


@login_required(login_url="/login")
def cart_remove(request, id):
    user=request.user
    cart = OrderItem.objects.get(id=id)

    menu=cart.menu
    initial_amount=cart.amount

    if not user.is_customer:
        amount=initial_amount - menu.price
    else:
        amount=initial_amount - menu.offer_price


    cart.amount=amount

    cart.qty -=1
    cart.save()

    if cart.qty == 0:
        cart.delete()
        

    return HttpResponseRedirect(reverse("customer:cart"))


@login_required(login_url="/login")
def orders(request):

    user= request.user
    pending_orders = Order.objects.filter(is_payement=False, user=user).all()
    completed_orders = Order.objects.filter(is_payement=True, user=user).all()

    context= {
        "title": "Canteen | Orders",
        "orders":completed_orders,
        "pendings":pending_orders,
        "user":user,
    }
    return render(request, "customer/orders.html", context=context)


login_required(login_url="/login")
def payment(request, id):

    user= request.user
    order = Order.objects.get(id=id)

    context= {
        "title": "Canteen | Orders",
        "order":order,
        "user":user,
    }
    return render(request, "customer/payment.html", context=context)


@login_required(login_url="/login")
def payment_card(request, id):
    user=request.user
    order = Order.objects.get(id=id)
    order.is_payement = True
    payment= Payment.objects.get(Order=order)
    payment.payment_done=True
    payment.save()
    order.save()
        

    return HttpResponseRedirect(reverse("customer:orders"))


@login_required(login_url="/login")
def payment_hand(request, id):
    user=request.user
    order = Order.objects.get(id=id)
    order.is_payement = False
    payment= Payment.objects.get(Order=order)
    payment.payment_done=True
    payment.save()
    order.save()
        

    return HttpResponseRedirect(reverse("customer:orders"))


@login_required(login_url="/login")
def feedback(request,id):
    user=request.user
    order= Order.objects.get(id=id)

    if request.method == "POST":
        title=request.POST.get("title")
        description=request.POST.get("description")
        
        if title and description:

            feedback = Feedback.objects.create(
                title = title,
                description = description,
                Order=order,
                user=user,
            )
            order.is_feedback=True
            order.save()

            feedback.save()

            return HttpResponseRedirect(reverse("customer:orders"))
        else:

            context= {
                "title": "Customer | Signup",
                "error": True,
                "message": "error occured",
                "order": order,
                "user": user
            }
    else:

        context= {
            "title": "Customer | Signup",
            "error": True,
            "message": "error occured",
            "order": order,
            "user":user
        }
    return render(request, "customer/feedback.html", context=context)


login_required(login_url="/login")
def feedback_view(request, id):

    user= request.user
    order = Order.objects.get(id=id)
    feedback = Feedback.objects.get(Order=order)

    context= {
        "title": "Canteen | Feedback",
        "feedback":feedback,
        "user":user,
        "order":order,
    }
    return render(request, "customer/feedback_view.html", context=context)