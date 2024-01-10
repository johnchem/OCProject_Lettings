import logging
from django.contrib import admin
from django.urls import path, include

from . import views

def trigger_error(request):
    division_by_zero = 1/0

def trigger_log(request):
    logging.debug("I am ignored")
    logging.info("I am a breadcrumb")
    logging.error("I am an event", extra=dict(bar=43))
    logging.exception("An exception happened")
    return views.index(request)

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
    path('404/', views.page_not_found),
    path('500/', views.server_error),
    path("sentry-debug/", trigger_error),
    path("logging-debug/", trigger_log),
]

# overwrite the default views for error 404 & 500
handler404 = "oc_lettings_site.views.page_not_found"
handler500 = "oc_lettings_site.views.server_error"