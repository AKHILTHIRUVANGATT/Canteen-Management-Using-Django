from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("manager/", include("manager.urls", namespace="manager")),
    path("kitchen/", include("kitchen.urls", namespace="kitchen")),
    path("staff/", include("staff.urls", namespace="staff")),
    path("", include("customer.urls", namespace="customer")),

]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
