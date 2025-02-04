from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractUser):
    mobile = models.CharField(null=True, blank=True, unique=True, error_messages={"unique":"Mobile number already used"})
    email = models.EmailField(null=True, blank=True, validators=[validate_email])
    is_manager= models.BooleanField('Is manager', default=False)
    is_waiter = models.BooleanField('Is waiter', default=False)
    is_kitchen = models.BooleanField('Is kitchen', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_guest = models.BooleanField('Is guest', default=False)


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return self.username
