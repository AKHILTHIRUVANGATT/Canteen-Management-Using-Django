from django import forms

from .models import Category, Menu
from user.models import User



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Category name"}),

        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "image", "price", "category", "description", "offer"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Item title"}),
            "description":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Item description"}),
            "price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Item price"}),
            "offer":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Item offer"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control","placeholder":"Image"}),
            "category":forms.widgets.Select(attrs={"class": "form-control"}),

        }



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","password","email","mobile"]

        widgets = {
            "first_name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Full name"}),
            "username":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Username"}),
            "password":forms.widgets.PasswordInput(attrs={"class": "form-control","placeholder":"Password"}),
            "email":forms.widgets.EmailInput(attrs={"class": "form-control","placeholder":"Email"}),
            "mobile":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Mobile"}),

        }