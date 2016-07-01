import datetime
import io
import json
import os

from backports import csv
from celery import shared_task, group
from celery.utils.log import get_task_logger

from api.models import Boats, Trips, Image
from api.utils.connection import get_connection_bucket, AWS_S3_CUSTOM_DOMAIN
from api.utils.funct_dates import (
    convert_str_in_datetime, convert_unix_in_datetime)
from api.utils.read_exif import (
    get_exif_dumps, get_exif_loads, convert_degress_to_decimal)
from django_mongo.celery import app

logger = get_task_logger(__name__)


@app.task
def prueba_suma(x, y):
    return x + y


@app.task
def prueba_resta(x, y):
    return x - y


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
                        mac_address=str(mac_address),
                        date=str(date),
                        longitude=str(picture_format.join()[0]['longitude']),
                        latitude=str(picture_format.join()[0]['latitude']),
                        image_filepath=path_dst,
                        datetime=str(picture_format.join()[0]['datetime'])
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
        trip.csv_filepath = ''
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
            url = "{0}temp/{1}".format(str(AWS_S3_CUSTOM_DOMAIN), str(string_picture))
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
    time = str(picture_format['datetime'].time())
    latitude = str(picture_format['latitude'])
    longitude = str(picture_format['longitude'])
    battery = str(picture_format['battery']) or '0'
    image_ = Image(image_filepath=path_dst, latitude=latitude, longitude=longitude,
                   orientation='', battery_level=battery, time=time)
    trip_obj.image.append(image_)
    trip_obj.save()


@app.task(trail=True)
def create_trip(list_folder):
    for a, b in list_folder.items():
        directory = b['directory']
        dst = 'media/uploads/container'
        geometry_list = b['geometry_list']
        mac_address_ = b['mac_address']
        date_ = b['date']
        dst_csv = "{0}/{1}/{2}.csv".format(str(dst), str(directory), str(directory))
        dst_json = "{0}/{1}/{2}.json".format(str(dst), str(directory), str(directory))

        for index, img in enumerate(geometry_list):
            path_dst = str(img['image_filepath'])
            mac_address = str(img['mac_address'])
            date_ = str(img['date'])
            boat = Boats.objects.filter(mac_address=mac_address)
            if not boat:
                trip = create_obj_trip(date_, mac_address, is_new=True)
                create_append_image(trip, img, path_dst)
            else:
                boat = Boats.objects.get(mac_address=mac_address)
                trip = create_obj_trip(date_, boat, is_new=False)
                create_append_image(trip, img, path_dst)

        boat = Boats.objects.get(mac_address=mac_address_)
        trip = Trips.objects.get(boat=boat, date=date_)
        trip.json_filepath = dst_json
        trip.csv_filepath = dst_csv
        trip.save()


@app.task(trail=True)
def task_create_json_file(list_folder, bucket_src):
    for a, b in list_folder.items():
        directory = b['directory']
        src = 'media/uploads/container/temp'
        geometry = b['geometry_list']
        dst = "{0}/{1}/{2}.json".format(str(src), str(directory), str(directory))
        k = bucket_src.new_key(dst)
        k.content_type = 'application/json'
        k.set_contents_from_string(json.dumps(geometry, indent=4))


@app.task(trail=True)
def write_csv(filename, rows):
    with io.open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["latitude", "longitude", "datetime"])
        for row in rows:
            writer.writerow([row["latitude"], row["longitude"], row["datetime"]])
        f.close()


@app.task()
def task_create_file_csv(list_folder, bucket_src):
    for a, b in list_folder.items():
        directory = b['directory']
        src = 'media/uploads/container/temp'
        geometry = b['geometry_list']
        dst = "{0}/{1}/{2}.csv".format(str(src), str(directory), str(directory))
        name_file = "{0}.csv".format(str(directory))
        write_csv(name_file, geometry)
        k = bucket_src.new_key(dst)
        k.content_type = 'text/csv'
        k.set_contents_from_filename(name_file)
        os.remove(name_file)


@app.task()
def task_move_parent_directory(list_folder, bucket_src):
    for a, b in list_folder.items():
        directory = b['directory']
        src = 'media/uploads/container'
        path_src = "{0}/temp/{1}/".format(str(src), str(directory))
        folders = bucket_src.list(prefix=path_src)

        for k in folders:
            if k.name:
                image_name = k.name.split("/")[-1]
                path_dst = "{0}/{1}/{2}".format(str(src), str(directory), str(image_name))

                bucket_src.lookup(k.name)
                bucket_src.copy_key(path_dst, bucket_src.name, k.name)
                bucket_src.delete_key(k.name)


@shared_task()
def run_folder():
    temp_list = get_temp_list_folder()
    list_folder = temp_list['folder_list']
    bucket_src = temp_list['bucket_src']
    now = datetime.datetime.now()
    logger.info("Task Start: result = %s" % str(now))
    create_trip(list_folder)
    task_create_json_file(list_folder, bucket_src)
    task_create_file_csv(list_folder, bucket_src)
    task_move_parent_directory(list_folder, bucket_src)
    now = datetime.datetime.now()
    logger.info("Task finished: result = %s" % str(now))
