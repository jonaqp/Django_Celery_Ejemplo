import io
import os
from api.models import Boats, Trips
from api.utils.connection import get_connection_bucket, AWS_S3_CUSTOM_DOMAIN
import urllib.request
from backports import csv

def create_file_csv(data):
    conn = get_connection_bucket()
    bucket_src = conn.get_bucket('shellcatch')
    src = 'media/uploads/container'

    for i, j in data.items():
        date = j['date']
        mac_address = j['mac_address']
        geometry = j['geometry']

        name_directory = "{0}_{1}".format(str(mac_address), str(date))
        name_file = "{0}.csv".format(str(name_directory))
        dst = "{0}/{1}/{2}.csv".format(str(src), str(name_directory), str(name_directory))
        url = "{0}{1}".format(AWS_S3_CUSTOM_DOMAIN, dst)
        try:
            data_request = urllib.request.urlopen(url).read().decode('utf8')
        except urllib.error.HTTPError as e:
            data_request = ''

        if data_request:
            urllib.request.urlretrieve(url, name_file)
            write_csv_add(name_file, geometry)
            k = bucket_src.new_key(dst)
            k.content_type = 'text/csv'
            k.set_contents_from_string(name_file)
            os.remove(name_file)

        else:

            write_csv(name_file, geometry)
            k = bucket_src.new_key(dst)
            k.content_type = 'text/csv'
            k.set_contents_from_filename(name_file)
            os.remove(name_file)

        boat = Boats.objects.get(mac_address=mac_address)
        trip = Trips.objects.get(boat=boat, date=date)
        trip.cvs_filepath = dst
        trip.save()


def write_csv_add(filename, rows):
    with io.open(filename, 'a+', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow([row["latitude"], row["longitude"], row["datetime"]])


def write_csv(filename, rows):
    with io.open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["latitude", "longitude", "datetime"])
        for row in rows:
            writer.writerow([row["latitude"], row["longitude"], row["datetime"]])
        f.close()


@app.task()
def task_create_json_file(list_folder, bucket_src):
    for a, b in list_folder.items():
        directory = b['directory']
        src = 'media/uploads/container/temp'
        geometry = b['geometry_list']
        dst = "{0}/{1}/{2}.json".format(str(src), str(directory), str(directory))
        k = bucket_src.new_key(dst)
        k.content_type = 'application/json'
        k.set_contents_from_string(json.dumps(geometry, indent=4))
