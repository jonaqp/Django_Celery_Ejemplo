from mongoengine import *

# connect(settings.MONGODB_NAME, host=settings.MONGODB_DATABASE_HOST)
connect('heroku_h0vjb9cj',
        host='mongodb://shellcatch_dev:shellcatch_password@ds025603.mlab.com:25603/heroku_h0vjb9cj')


class Buckets(Document):
    bucket_name = StringField(max_length=255)
    bucket_access_key = StringField(max_length=255)
    bucket_secret_key = StringField(max_length=255)
    bucket_path_image = StringField(max_length=255)


class Events(EmbeddedDocument):
    name = StringField(max_length=50)
    time_start = StringField(max_length=100)
    time_end = StringField(max_length=100)
    comments = StringField(max_length=255)
    supervisor = StringField(max_length=100)


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
    time = StringField(max_length=50)
    image_filepath = StringField(max_length=255)
    latitude = StringField(max_length=20)
    longitude = StringField(max_length=20)
    orientation = StringField(max_length=10)
    battery_level = StringField(max_length=10)


class Boats(Document):
    mac_address = StringField(max_length=50)
    country = EmbeddedDocumentField(Country)
    company = EmbeddedDocumentField(Company)
    phone = EmbeddedDocumentField(Phone)
    port = EmbeddedDocumentField(Port)


class Trips(Document):
    boat = ReferenceField(Boats)
    mac_address = StringField(max_length=50)
    date = StringField(max_length=50)
    json_filepath = StringField(max_length=255)
    txt_filepath = StringField(max_length=255)
    csv_filepath = StringField(max_length=255)
    video_filepath = StringField(max_length=255)
    image = ListField(EmbeddedDocumentField(Image))
    events = EmbeddedDocumentField(Events)
