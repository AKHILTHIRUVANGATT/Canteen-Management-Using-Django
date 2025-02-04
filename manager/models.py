from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)


    class Meta:
        db_table = 'manager_manager'
        verbose_name = 'manager'
        verbose_name_plural = 'managers'
        ordering = ('id',)

    def __str__(self):

        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'manager_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('id',)

    def __str__(self):

        return self.name
    

class Menu(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="menu")
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'is_deleted':False})
    offer = models.IntegerField()
    offer_price = models.FloatField()
    description = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)


    class Meta:
        db_table = 'manager_menu'
        verbose_name = 'menu'
        verbose_name_plural = 'menus'
        ordering = ('id',)

    def __str__(self):

        return self.name