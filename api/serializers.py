from __future__ import division, unicode_literals

from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from .models import Boats, Trips, Image


class BoatSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Boats
        depth = 2


class BoatCreateUpdateSerializer(DocumentSerializer):
    class Meta:
        model = Boats
        fields = ('mac_address',)
        depth = 2


class TripSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Trips
        depth = 2


class ImageSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Image
        fields = ('image_filepath', 'latitude', 'longitude', 'orientation', 'battery_level',)
        depth = 2


class TripCreateUpdateSerializer(DocumentSerializer):
    mac_address = serializers.CharField()
    image = ImageSerializer(many=True, required=False)

    # datetime = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Trips
        fields = ('mac_address', 'date', 'time', 'json_filepath', 'image',)
        depth = 2

    def create(self, validated_data):
        print(validated_data)
        return super(TripCreateUpdateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        images = validated_data.pop('image')
        updated_instance = super(TripCreateUpdateSerializer, self).update(instance, validated_data)
        for image_data in images:
            updated_instance.image.append(images(**image_data))
        updated_instance.save()
        return updated_instance
