from __future__ import division, unicode_literals

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from .models import Boats, Buckets


class BoatSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Boats
        depth = 2


class BoatCreateUpdateSerializer(DocumentSerializer):
    class Meta:
        model = Boats
        fields = ('mac_address',)
        depth = 2


class BucketSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Buckets
        depth = 2


class BucketCreateUpdateSerializer(DocumentSerializer):
    class Meta:
        model = Buckets
        fields = ('bucket_name', 'bucket_access_key', 'bucket_secret_key', 'bucket_path_image')
        depth = 2
