from .models import Boats, Buckets
from django.views.generic import TemplateView
from rest_framework_mongoengine.generics import (
    ListAPIView, CreateAPIView)
from .serializers import (
    BoatSerializer,
    BoatCreateUpdateSerializer,
    BucketSerializer,
    BucketCreateUpdateSerializer
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BoatCreateAPIView(CreateAPIView):
    queryset = Boats.objects.all()
    serializer_class = BoatCreateUpdateSerializer


class BoatListAPIView(ListAPIView):
    queryset = Boats.objects.all()
    serializer_class = BoatSerializer


class BucketListAPIView(ListAPIView):
    queryset = Buckets.objects.all()
    serializer_class = BucketSerializer


class BucketCreateAPIView(CreateAPIView):
    queryset = Buckets.objects.all()
    serializer_class = BucketCreateUpdateSerializer