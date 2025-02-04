from django.db import models


class Staff(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'staff_staff'
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'
        ordering = ('id',)

    def __str__(self):

        return self.name