from django.conf.urls import url

from .views import (
    IndexView,
    BoatListAPIView,
    # BoatCreateAPIView,
    TripListAPIView,
    # TripCreateAPIView,
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='api-task'),
    url(r'boat/$', BoatListAPIView.as_view(), name='boat'),
    # url(r'boat/create/$', BoatCreateAPIView.as_view(), name='api-container-create'),
    url(r'trip/$', TripListAPIView.as_view(), name='trip'),
    # url(r'trip/create/$', TripCreateAPIView.as_view(), name='api-container-create'),

]
