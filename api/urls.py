from django.conf.urls import url

from .views import (
    IndexView,
    BoatListAPIView,
    BucketListAPIView,
    BucketCreateAPIView

)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='api-task'),
    url(r'boat/$', BoatListAPIView.as_view(), name='boat'),
    url(r'bucket/$', BucketListAPIView.as_view(), name='bucket'),
    url(r'bucket/create/$', BucketCreateAPIView.as_view(), name='bucket-create'),
]
