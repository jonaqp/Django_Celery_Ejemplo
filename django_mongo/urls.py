from django.conf.urls import url
from django.contrib import admin

from api.views import IndexView

urlpatterns = [
    url(r'^index/', IndexView.as_view(), name='index1'),
    url(r'^$', IndexView.as_view(), name='index2'),
    url(r'^admin/', admin.site.urls),
]
