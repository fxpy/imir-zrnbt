from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.sites.models import Site

from main.views import update

urlpatterns = [
    path('', admin.site.urls),
    path(settings.TOKEN, update),
]

# admin.autodiscover()
admin.site.unregister(Site)
