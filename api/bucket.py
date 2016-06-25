import boto.s3.connection
from api.models import Boat, Trip, Image
from api.utils.funct_dates import (
    convert_str_in_datetime, convert_unix_in_datetime)
from api.utils.read_exif import (
    get_exif_dumps, get_exif_loads, convert_degress_to_decimal)

AWS_STORAGE_BUCKET_NAME = 'shellcatch'
AWS_S3_CUSTOM_DOMAIN = 'https://{0:s}.s3.amazonaws.com/'.format(str(AWS_STORAGE_BUCKET_NAME))
AWS_ACCESS_KEY_ID = 'AKIAJRA5Z7OCTBF7JPNA'
AWS_SECRET_ACCESS_KEY = '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'


def get_validate_format(string_picture):
    image_ = string_picture.split("/")[-1]
    file_base = image_.split("_")

    if len(file_base) == 8:
        mac_address = file_base[1]
        new_datetime = convert_str_in_datetime(convert_unix_in_datetime(file_base[3]))
        latitude = float(file_base[4][3:])
        longitude = float(file_base[5][3:])
        result = dict(datetime=new_datetime, mac_address=mac_address, is_new=False,
                      latitude=latitude, longitude=longitude, battery='')
        return result

    if len(file_base) == 5:
        string_val = str(file_base[-1].split('.')[0])
        if not string_val == 'ori0':
            mac_address = file_base[1]
            picture_date = "{0}-{1}-{2}".format(str(file_base[2]),
                                                str(file_base[3]),
                                                str(file_base[4].split(".")[0].split("-")[0]))
            picture_hour = "{0}:{1}:{2}".format(str(file_base[4].split(".")[0].split("-")[1]),
                                                str(file_base[4].split(".")[0].split("-")[2]),
                                                str(file_base[4].split(".")[0].split("-")[3]))
            string_datetime_now = "{0} {1}".format(str(picture_date), str(picture_hour))
            url = "{0}{1}".format(str(AWS_S3_CUSTOM_DOMAIN), str(string_picture))
            url_exif_data = get_exif_dumps(url)
            metadata_latitude = get_exif_loads(url_exif_data)[0]['exif:GPSLatitude']
            metadata_longitude = get_exif_loads(url_exif_data)[0]['exif:GPSLongitude']
            metadata_batterylevel = str(get_exif_loads(url_exif_data)[0]['exif:BatteryLevel'])
            latitude = convert_degress_to_decimal(metadata_latitude)
            longitude = convert_degress_to_decimal(metadata_longitude)
            new_datetime = convert_str_in_datetime(string_datetime_now)
            result = dict(datetime=new_datetime, mac_address=mac_address, is_new=True,
                          latitude=latitude, longitude=longitude, battery=metadata_batterylevel)
            return result
        else:
            mac_address = file_base[1]
            new_datetime = convert_str_in_datetime(convert_unix_in_datetime(file_base[3]))
            latitude = ''
            longitude = ''
            result = dict(datetime=new_datetime, mac_address=mac_address, is_new=False,
                          latitude=latitude, longitude=longitude, battery='')
            return result


def create_append_image(trip_obj, picture_format, path_dst):
    latitude = str(picture_format['latitude'])
    longitude = str(picture_format['longitude'])
    battery = str(picture_format['battery'])
    image_ = Image(image_filepath=path_dst, latitude=latitude, longitude=longitude,
                   orientation='', battery_level=battery)
    trip_obj.image.append(image_)
    trip_obj.save()


def create_trip(picture, path_dst):
    picture_format = get_validate_format(str(picture))
    mac_address = picture_format['mac_address']
    date_time = picture_format['datetime']
    date_ = str(date_time.date())
    time_ = str(date_time.time())
    boat = Boat.objects.filter(mac_address=mac_address)

    if not boat:
        print("here1")
        trip = Trip.create(date_, time_, mac_address, is_new=True)
        create_append_image(trip, picture_format, path_dst)
    else:
        print("here2")
        boat = Boat.objects.get(mac_address=mac_address)
        trip = Trip.create(date_, time_, boat, is_new=False)
        create_append_image(trip, picture_format, path_dst)
    return picture_format


def load_image():
    conn = boto.connect_s3(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
    bucket_src = conn.get_bucket('shellcatch')
    src = 'media/uploads/container/temp/'
    dst = 'media/uploads/container/'
    folders = bucket_src.list(prefix=src, delimiter='.jpg')
    for k in folders:
        extension_correct = k.name.endswith(('.jpg', '.jpeg'))
        if extension_correct:
            image_name = k.name.split("/")[-1]
            image_directory = k.name.split("/")[-2]
            path_dst = "{0}{1}/{2}".format(str(dst), str(image_directory), str(image_name))
            name = k.name
            create_trip(name, path_dst)
            bucket_src.lookup(k.name)
            bucket_src.copy_key(path_dst, bucket_src.name, k.name)
            bucket_src.delete_key(k.name)
    return str('Successfull')


if __name__ == "__main__":
    load_image()
