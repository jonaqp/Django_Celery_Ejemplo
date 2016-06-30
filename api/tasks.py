import datetime

from celery import shared_task, group
from celery.utils.log import get_task_logger
# from api.bucket import load_image
from api.utils.connection import get_connection_bucket
from django_mongo.celery import app
from api.models import Boats, Trips, Image
from api.utils.funct_dates import (
    convert_str_in_datetime, convert_unix_in_datetime)
from api.utils.read_exif import (
    get_exif_dumps, get_exif_loads, convert_degress_to_decimal)
logger = get_task_logger(__name__)


@app.task
def prueba_suma(x, y):
    return x + y


@app.task
def prueba_resta(x, y):
    return x - y


@shared_task()
def fetch_url():
    scraper_example()


def scraper_example():
    logger.info("Start task")
    # a = load_image()
    now = datetime.datetime.now()
    logger.info("Task finished: result = %s" % str(now))


@app.task(trail=True)
def get_temp_list_folder():
    conn = get_connection_bucket()
    bucket_src = conn.get_bucket('shellcatch')
    src = 'media/uploads/container/temp/'
    dst = 'media/uploads/container'
    folders = bucket_src.list(prefix=src, delimiter='/')
    result_list = list()
    for k in folders:
        name = k.name.split("/")[-2]
        result_list.append(name)
    new_result = result_list[1:]
    result_image_dict = dict()
    for i in new_result:
        directory = str(i)
        mac_address = directory.split("_")[0]
        date = directory.split("_")[1]
        src = "{0}/{1}".format(str('media/uploads/container/temp'), str(i))
        folders = bucket_src.list(prefix=src)
        for k in folders:
            extension_correct = k.name.endswith(('.jpg', '.jpeg'))
            if extension_correct:
                image_name = k.name.split("/")[-1]
                picture_format = group(get_validate_format.s(str(image_name))).apply_async()
                if picture_format.successful():
                    path_dst = "{0}/{1}/{2}".format(str(dst), str(directory), str(image_name))
                    if i not in result_image_dict.keys():
                        result_image_dict[i] = dict(directory='', mac_address='', date='',
                                                    image_list=list(), geometry_list=list())
                    result_image_dict[i]['directory'] = directory
                    result_image_dict[i]['mac_address'] = mac_address
                    result_image_dict[i]['date'] = date
                    result_image_dict[i]['image_list'].append(image_name)
                    result_image_dict[i]['geometry_list'].append(
                        dict(
                            longitude=str(picture_format.get()[0]['longitude']),
                            latitude=str(picture_format.get()[0]['latitude']),
                            image_filepath=path_dst,
                            datetime=str(picture_format.get()[0]['datetime'])
                        )
                    )

    result = dict(folder_list=result_image_dict, bucket_src=bucket_src)
    return result


@app.task(trail=True)
def create_obj_boat(mac_address):
    boat = Boats()
    boat.mac_address = mac_address
    boat.save()
    return boat


@app.task(trail=True)
def create_obj_trip(date_image, mac_address, is_new=True):
    new_boat = mac_address
    if mac_address and is_new:
        new_boat = create_obj_boat(mac_address)
        trip = Trips()
        trip.date = date_image
        trip.json_filepath = ''
        trip.cvs_filepath = ''
        trip.video_filepath = ''
        trip.boat = new_boat
        trip.mac_address = new_boat.mac_address
        trip.save()
        return trip
    elif mac_address and not is_new:
        new_boat = new_boat
        trip = Trips.objects.filter(boat=new_boat, date=date_image)
        if trip:
            trip = Trips.objects.get(boat=new_boat, date=date_image)
        else:
            trip = Trips()
            trip.date = date_image
            trip.json_filepath = ''
            trip.cvs_filepath = ''
            trip.video_filepath = ''
            trip.boat = new_boat
            trip.mac_address = new_boat.mac_address
            trip.save()
        return trip


@app.task(trail=True)
def get_validate_format(string_picture):
    image_ = string_picture.split("/")[-1]
    file_base = image_.split("_")
    result = dict()
    if len(file_base) == 8:
        mac_address = file_base[1]
        new_datetime = convert_str_in_datetime(convert_unix_in_datetime(file_base[3]))
        latitude = float(file_base[4][3:])
        longitude = float(file_base[5][3:])
        result = dict(datetime=new_datetime, mac_address=mac_address, is_new=False,
                      latitude=latitude, longitude=longitude, battery='')
    if len(file_base) == 5:
        string_val = str(file_base[-1].split('.')[0])
        if string_val not in ('ori0', 'ori1', 'ori2', 'ori3', 'ori4', 'ori5', 'ori6'):
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
        else:
            mac_address = file_base[1]
            new_datetime = convert_str_in_datetime(convert_unix_in_datetime(file_base[3]))
            latitude = ''
            longitude = ''
            result = dict(datetime=new_datetime, mac_address=mac_address, is_new=False,
                          latitude=latitude, longitude=longitude, battery='')
    return result


@app.task(trail=True)
def create_append_image(trip_obj, picture_format, path_dst):
    time = str(picture_format.join()[0]['datetime'].time())
    latitude = str(picture_format.join()[0]['latitude'])
    longitude = str(picture_format.join()[0]['longitude'])
    battery = str(picture_format.join()[0]['battery']) or '0'
    image_ = Image(image_filepath=path_dst, latitude=latitude, longitude=longitude,
                   orientation='', battery_level=battery, time=time)
    trip_obj.image.append(image_)
    trip_obj.save()


@app.task(trail=True)
def create_trip(list_folder):
    for a, b in list_folder.items():
        directory = b['directory']
        dst = 'media/uploads/container'
        image_list = b['image_list']

        for img in image_list:
            path_dst = "{0}/{1}/{2}".format(str(dst), str(directory), str(img))
            picture_format = group(get_validate_format.s(str(img))).apply_async()
            if picture_format.successful():
                mac_address = str(picture_format.get()[0]['mac_address'])
                date_time = picture_format.join()[0]['datetime']
                date_ = str(date_time.date())
                boat = Boats.objects.filter(mac_address=mac_address)

                if not boat:
                    trip = create_obj_trip(date_, mac_address, is_new=True)
                    create_append_image(trip, picture_format, path_dst)
                else:
                    boat = Boats.objects.get(mac_address=mac_address)
                    trip = create_obj_trip(date_, boat, is_new=False)
                    create_append_image(trip, picture_format, path_dst)

