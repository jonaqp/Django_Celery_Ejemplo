from django.conf.urls import url, include
from django.contrib import admin

from api.views import IndexView

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^$', include('api.urls')),
    url(r'^admin/', admin.site.urls),

]
