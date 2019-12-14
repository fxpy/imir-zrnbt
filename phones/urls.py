from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.sites.models import Site

from main.views import update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', update),
]

# admin.autodiscover()
admin.site.unregister(Site)