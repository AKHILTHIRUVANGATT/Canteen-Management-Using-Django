import datetime

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_staff
from main.functions import generate_form_errors

from manager.models import Manager, Category, Menu
from customer.models import Customer, Order, Payment, Feedback
from kitchen.models import Kitchen
from staff.models import Staff
from manager.forms import CategoryForm, ItemForm, UserForm
from user.models import User


@login_required(login_url='/staff/login')
@allow_staff
def orders(request):
    user=request.user
    staff= Staff.objects.get(user=user)
    orders = Order.objects.filter(is_prepared=True, staff=staff)
    conntext = {
        "title": "Staff Dashboard",
        "orders":orders,
    }
    return render(request, 'staff/orders.html', context=conntext)


@login_required(login_url='/staff/login')
@allow_staff
def order_serv(request,id):
    user=request.user
    staff= Staff.objects.get(user=user)
    instance = get_object_or_404(Order, id=id)
    instance.is_prepared=False
    instance.is_completed=True
    staff.is_active=True
    staff.save()
    instance.save()

    return HttpResponseRedirect(reverse("staff:orders"))


@login_required(login_url='/staff/login')
@allow_staff
def order_view(request, id):
    order = get_object_or_404(Order, id=id)
    conntext = {
        "title": "Staff Dashboard",
        "order":order,

    }
    return render(request, 'staff/items.html', context=conntext)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_waiter:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("staff:orders"))
            else:
                context= {
                    "title": "staff Login | Home",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "staff/login.html", context=context)
        else:
            context= {
                "title": "staff Login | Home",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "staff/login.html", context=context)
    else:
        context= {
            "title" : "staff Login | Home"
        }
        return render(request, "staff/login.html", context=context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("staff:login"))


@login_required(login_url='/staff/login')
@allow_staff
def account(request):
    user=request.user
    staff= Staff.objects.get(user=user)

    context= {
        "title": "Staff Dashboard | Account",
        "sub_tittle": "Profile",
        "name": "My Account",
        "staff":staff,
    }
    return render(request, "staff/account.html", context=context)