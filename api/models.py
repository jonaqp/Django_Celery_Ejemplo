from django.conf import settings
from mongoengine import *
connect(settings.MONGODB_NAME, host=settings.MONGODB_DATABASE_HOST)
# connect('heroku_h0vjb9cj',
#         host='mongodb://shellcatch_dev:shellcatch_password@ds025603.mlab.com:25603/heroku_h0vjb9cj')


class Port(EmbeddedDocument):
    name = StringField(max_length=50)
    description = StringField(max_length=100)


class Phone(EmbeddedDocument):
    location = StringField(max_length=50)
    code = StringField(max_length=50)
    number = StringField(max_length=50)


class Company(EmbeddedDocument):
    name = StringField(max_length=50)
    logo = StringField(max_length=50)
    address = StringField(max_length=50)
    phone = StringField(max_length=50)


class Country(EmbeddedDocument):
    zone = StringField(max_length=50)
    name = StringField(max_length=50)
    code = StringField(max_length=50)


class Image(EmbeddedDocument):
    image_filepath =  StringField(max_length=255)
    latitude = StringField(max_length=20)
    longitude = StringField(max_length=20)
    orientation = StringField(max_length=10)
    battery_level = StringField(max_length=10)


class Boat(Document):
    mac_address = StringField(max_length=50)
    country = EmbeddedDocumentField(Country)
    company = EmbeddedDocumentField(Company)
    phone = EmbeddedDocumentField(Phone)
    port = EmbeddedDocumentField(Port)

    @staticmethod
    def create(mac_address):
        boat = Boat()
        boat.mac_address = mac_address
        boat.save()
        return boat


class Trip(Document):
    mac_address = ReferenceField(Boat)
    date = StringField(max_length=50)
    time = StringField(max_length=50)
    json_filepath = URLField()
    image = ListField(EmbeddedDocumentField(Image))

    @staticmethod
    def create(date_image, time_image, mac_address, is_new=True):
        new_mac_address = mac_address
        if mac_address and is_new:
            new_mac_address = Boat.create(mac_address)
            trip = Trip()
            trip.date = date_image
            trip.time = time_image
            trip.mac_address = new_mac_address
            trip.save()
            return trip
        elif mac_address and not is_new:
            new_mac_address = new_mac_address
            trip = Trip.objects.filter(mac_address=new_mac_address, date=date_image)
            if trip:
                trip = Trip.objects.get(mac_address=new_mac_address, date=date_image)
            else:
                trip = Trip()
                trip.date = date_image
                trip.time = time_image
                trip.mac_address = new_mac_address
                trip.save()
            return trip
