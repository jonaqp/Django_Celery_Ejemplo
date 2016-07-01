from .models import Boats, Trips
from django.views.generic import TemplateView
from rest_framework_mongoengine.generics import (
    ListAPIView, CreateAPIView)
from .serializers import (
    BoatSerializer,
    BoatCreateUpdateSerializer,
    TripSerializer,
    TripCreateUpdateSerializer,
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


class TripCreateAPIView(CreateAPIView):
    queryset = Trips.objects.all()
    serializer_class = TripCreateUpdateSerializer


class TripListAPIView(ListAPIView):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
