import datetime

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse

from main.decorators import allow_manager
from main.functions import generate_form_errors

from .models import Manager, Category, Menu
from customer.models import Customer, Order, Payment, Feedback, OrderItem
from kitchen.models import Kitchen
from staff.models import Staff
from .forms import CategoryForm, ItemForm, UserForm
from user.models import User


@login_required(login_url="/manager/login")
@allow_manager
def index(request):
    orders = Order.objects.all().count()
    items = Menu.objects.all().count()
    customers = Customer.objects.all().count()
    payments = Payment.objects.all().count()
    conntext = {
        "title": "Manager Dashboard",
        "orders":orders,
        "items":items,
        "customers":customers,
        "payments":payments,
    }
    return render(request, 'manager/index.html', context=conntext)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_manager:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("manager:index"))
            else:
                context= {
                    "title": "Manager Login | Home",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "manager/login.html", context=context)
        else:
            context= {
                "title": "Manager Login | Home",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "manager/login.html", context=context)
    else:
        context= {
            "title" : "Manager Login | Home"
        }
        return render(request, "manager/login.html", context=context)



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("manager:login"))



@login_required(login_url="/manager/login")
@allow_manager
def account(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    context= {
        "title": "Manager Dashboard | Account",
        "sub_tittle": "Profile",
        "name": "My Account",
        "manager":manager,
    }
    return render(request, "manager/account.html", context=context)



@login_required(login_url="/manager/login")
@allow_manager
def category(request):
    categories= Category.objects.all()

    context= {
        "title": "Manager Dashboard | Category",
        "sub_tittle": "Category",
        "name": "Category",
        "categories":categories,
    }
    return render(request, "manager/categories.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def category_add(request):

    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("manager:category"))
        else:
            message = generate_form_errors(form)
            form = CategoryForm()
            context= {
                "title": "Manager Dashboard | Category",
                "sub_tittle": "Category",
                "name": "Category Add",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/category-add.html", context=context)

    else:
        form = CategoryForm()
        context= {
            "title": "Manager Dashboard | Category",
            "sub_tittle": "Category",
            "name": "Category Add",
            "form": form,
        }
        return render(request, "manager/category-add.html", context=context)
    

@login_required(login_url="/manager/login")
@allow_manager
def items(request):
    items= Menu.objects.all()

    context= {
        "title": "Manager Dashboard | Items",
        "sub_tittle": "Items",
        "name": "Items",
        "items":items,
    }
    return render(request, "manager/items.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def items_add(request):

    if request.method == "POST":
        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            price = instance.price
            offer = instance.offer
            if offer > 0:
                offer_price = price * ((100-offer)/100)
            else:
                offer_price=price

            instance.offer_price=offer_price
            instance.save()


            return HttpResponseRedirect(reverse("manager:items"))
        else:
            message = generate_form_errors(form)
            form = ItemForm()
            context= {
                "title": "Manager Dashboard | Item",
                "sub_tittle": "Item",
                "name": "Item Add",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/items-add.html", context=context)

    else:
        form = ItemForm()
        context= {
            "title": "Manager Dashboard | Item",
            "sub_tittle": "Item",
            "name": "Item Add",
            "form": form,
        }
        return render(request, "manager/items-add.html", context=context)
    


@login_required(login_url="/manager/login")
@allow_manager
def items_edit(request, id):
    instance = get_object_or_404(Menu, id=id)

    if request.method == "POST":
        form = ItemForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            price = instance.price
            offer = instance.offer
            if offer > 0:
                offer_price = price * ((100-offer)/100)
            else:
                offer_price=price
            instance.offer_price=offer_price
            instance.save()

            return HttpResponseRedirect(reverse("manager:items"))
        else:
            message = generate_form_errors(form)
            form = ItemForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Item",
                "sub_tittle": "Item",
                "name": "Item Add",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/items-add.html", context=context)

    else:
        form = ItemForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Item",
            "sub_tittle": "Item",
            "name": "Item Add",
            "form": form,
        }
        return render(request, "manager/items-add.html", context=context)
    

@login_required(login_url="/manager/login")
@allow_manager
def items_enable(request,id):
    instance = get_object_or_404(Menu, id=id)
    instance.is_active = True
    instance.save()

    return HttpResponseRedirect(reverse("manager:items"))


@login_required(login_url="/manager/login")
@allow_manager
def items_disable(request,id):
    instance = get_object_or_404(Menu, id=id)
    instance.is_active = False
    instance.save()

    return HttpResponseRedirect(reverse("manager:items"))


@login_required(login_url="/manager/login")
@allow_manager
def offers(request):
    offers= Menu.objects.all()

    context= {
        "title": "Manager Dashboard | offers",
        "sub_tittle": "offers",
        "name": "offers",
        "offers":offers,
    }
    return render(request, "manager/offers.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def orders(request):
    orders= Order.objects.all()

    context= {
        "title": "Manager Dashboard | Orders",
        "sub_tittle": "Orders",
        "name": "Orders",
        "orders":orders,
    }
    return render(request, "manager/orders.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def payments(request):
    payments= Payment.objects.all()

    context= {
        "title": "Manager Dashboard | Payments",
        "sub_tittle": "Payments",
        "name": "Payments",
        "payments":payments,
    }
    return render(request, "manager/payments.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def payments_cmpt(request,id):
    instance = get_object_or_404(Payment, id=id)
    instance.payment_done = True
    order = instance.Order
    order.is_payement = True
    order.is_prepared= False
    order.save()
    instance.save()

    return HttpResponseRedirect(reverse("manager:payments"))


@login_required(login_url="/manager/login")
@allow_manager
def feedbacks(request):
    feedbacks= Feedback.objects.all()

    context= {
        "title": "Manager Dashboard | Feedbacks",
        "sub_tittle": "Feedbacks",
        "name": "Feedbacks",
        "feedbacks":feedbacks,
    }
    return render(request, "manager/feedbacks.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def staffs(request):
    staffs= Staff.objects.all()

    context= {
        "title": "Manager Dashboard | Staffs",
        "sub_tittle": "Staffs",
        "name": "Staffs",
        "staffs":staffs,
    }
    return render(request, "manager/staffs.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def staffs_add(request):

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            user = User.objects.create_user(
                username = instance.username,
                password = instance.password,
                email = instance.email,
                first_name = instance.first_name,
                mobile = instance.mobile,
                is_waiter=True
            )

            staff = Staff.objects.create(
                user=user,
                name=user.first_name,
            )
            staff.save()

            user.save()

            return HttpResponseRedirect(reverse("manager:staffs"))
        else:
            message = generate_form_errors(form)
            form = UserForm()
            context= {
                "title": "Manager Dashboard | Staff",
                "sub_tittle": "Staff",
                "name": "Staff Add",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/staffs-add.html", context=context)

    else:
        form = UserForm()
        context= {
            "title": "Manager Dashboard | Staff",
            "sub_tittle": "Staff",
            "name": "Staff Add",
            "form": form,
        }
        return render(request, "manager/staffs-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def kitchens(request):
    kitchens= Kitchen.objects.all()

    context= {
        "title": "Manager Dashboard | kitchens",
        "sub_tittle": "kitchens",
        "name": "kitchens",
        "kitchens":kitchens,
    }
    return render(request, "manager/kitchens.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def kitchens_add(request):

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            user = User.objects.create_user(
                username = instance.username,
                password = instance.password,
                email = instance.email,
                first_name = instance.first_name,
                mobile = instance.mobile,
                is_kitchen=True
            )

            kitchen = Kitchen.objects.create(
                user=user,
                name=user.first_name,
            )
            kitchen.save()
            user.save()

            return HttpResponseRedirect(reverse("manager:kitchens"))
        else:
            message = generate_form_errors(form)
            form = UserForm()
            context= {
                "title": "Manager Dashboard | Kitchen",
                "sub_tittle": "Kitchen",
                "name": "Kitchen Add",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/staffs-add.html", context=context)

    else:
        form = UserForm()
        context= {
            "title": "Manager Dashboard | Kitchen",
            "sub_tittle": "Kitchen",
            "name": "Kitchen Add",
            "form": form,
        }
        return render(request, "manager/staffs-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def customers(request):
    customers= Customer.objects.all()

    context= {
        "title": "Manager Dashboard | Customers",
        "sub_tittle": "Customers",
        "name": "Customers",
        "customers":customers,
    }
    return render(request, "manager/customers.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def customers_by(request):
    customers= Customer.objects.all()

    context= {
        "title": "Manager Dashboard | Order",
        "sub_tittle": "Order",
        "name": "Order",
        "customers":customers,
    }
    return render(request, "manager/by-customers.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def order_customer(request, id):
    customer= Customer.objects.get(id=id)

    user=customer.user

    orders = Order.objects.filter(user=user, is_completed=True)

    context= {
        "title": "Manager Dashboard | Order",
        "sub_tittle": "Order",
        "name": "Order",
        "orders":orders,
    }
    return render(request, "manager/orders-customers.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def items_date(request):
    items= Menu.objects.all()

    context= {
        "title": "Manager Dashboard | Items",
        "sub_tittle": "Items",
        "name": "Items",
        "items":items,
    }
    return render(request, "manager/items-date.html", context=context)



@login_required(login_url="/manager/login")
@allow_manager
def order_date(request,id):

    item = Menu.objects.get(id=id)

    orders_count = OrderItem.objects.filter(menu=item).count()

    orders = OrderItem.objects.filter(menu=item)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        orders = orders.filter(created_date__range=(start_date,end_date))
        orders_count = orders.filter(menu=item).count()

    context= {
        "title": "Manager Dashboard | Order",
        "sub_tittle": "Order",
        "name": "Order",
        "orders":orders,
        "start_date":start_date,
        "end_date":end_date,
        "orders_count":orders_count,
        "item":item,
    }
    return render(request, "manager/orders-date.html", context=context)



@login_required(login_url="/manager/login")
@allow_manager
def graph(request):
    items= Menu.objects.all()

    context= {
        "title": "Manager Dashboard | Graph",
        "sub_tittle": "Graph",
        "name": "Graphical Representation",
        "items":items,
    }
    return render(request, "manager/graph.html", context=context)


def population_chart(request):
    labels = []
    data = []

    items = Menu.objects.all()

    for item in items:
        labels.append(item)

        count = OrderItem.objects.filter(menu=item).count()

        data.append(count)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
