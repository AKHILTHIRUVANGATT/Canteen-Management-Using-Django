from django.db import models


class Kitchen(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)


    class Meta:
        db_table = 'kitchen_kitchen'
        verbose_name = 'kitchen'
        verbose_name_plural = 'kitchens'
        ordering = ('id',)

    def __str__(self):

        return self.name