from django.conf.urls import url
from django.contrib import admin

from api.views import index

urlpatterns = [
    url(r'^index/', index),
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
]
