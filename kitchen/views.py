import datetime

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_kitchen
from main.functions import generate_form_errors

from manager.models import Manager, Category, Menu
from customer.models import Customer, Order, Payment, Feedback
from kitchen.models import Kitchen
from staff.models import Staff
from manager.forms import CategoryForm, ItemForm, UserForm
from user.models import User


@login_required(login_url='/kitchen/login')
@allow_kitchen
def orders(request):
    orders = Order.objects.filter(is_pending=True)
    conntext = {
        "title": "Kitchen Dashboard",
        "orders":orders,
    }
    return render(request, 'kitchen/orders.html', context=conntext)


@login_required(login_url='/kitchen/login')
@allow_kitchen
def order_pre(request,id):
    staff = Staff.objects.filter(is_active=True)[:1].get()
    instance = get_object_or_404(Order, id=id)
    instance.is_pending = False
    instance.is_prepared=True
    instance.staff=staff
    staff.is_active=False
    staff.save()
    instance.save()

    return HttpResponseRedirect(reverse("kitchen:orders"))


@login_required(login_url='/kitchen/login')
@allow_kitchen
def order_view(request,id):
    order = get_object_or_404(Order, id=id)
    conntext = {
        "title": "Kitchen Dashboard",
        "order":order,

    }
    return render(request, 'kitchen/items.html', context=conntext)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_kitchen:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("kitchen:orders"))
            else:
                context= {
                    "title": "Kitchen Login | Home",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "kitchen/login.html", context=context)
        else:
            context= {
                "title": "Kitchen Login | Home",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "kitchen/login.html", context=context)
    else:
        context= {
            "title" : "Kitchen Login | Home"
        }
        return render(request, "kitchen/login.html", context=context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("kitchen:login"))



@login_required(login_url="/kitchen/login")
@allow_kitchen
def account(request):
    user=request.user
    kitchen= Kitchen.objects.get(user=user)

    context= {
        "title": "Kitchen Dashboard | Account",
        "sub_tittle": "Profile",
        "name": "My Account",
        "kitchen":kitchen,
    }
    return render(request, "kitchen/account.html", context=context)


@login_required(login_url='/kitchen/login')
@allow_kitchen
def items(request):
    items= Menu.objects.all()

    context= {
        "title": "Kitchen Dashboard | Items",
        "sub_tittle": "Items",
        "name": "Items",
        "items":items,
    }
    return render(request, "kitchen/item.html", context=context)


@login_required(login_url='/kitchen/login')
@allow_kitchen
def items_enable(request,id):
    instance = get_object_or_404(Menu, id=id)
    instance.is_active = True
    instance.save()

    return HttpResponseRedirect(reverse("kitchen:items"))


@login_required(login_url='/kitchen/login')
@allow_kitchen
def items_disable(request,id):
    instance = get_object_or_404(Menu, id=id)
    instance.is_active = False
    instance.save()

    return HttpResponseRedirect(reverse("kitchen:items"))