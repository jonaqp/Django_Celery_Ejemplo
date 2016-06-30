import io
import json
import os
import datetime as datetimex

import boto.s3.connection
from backports import csv

from api.models import Boats, Trips, Image
from api.utils.funct_dates import (
    convert_str_in_datetime, convert_unix_in_datetime)
from api.utils.read_exif import (
    get_exif_dumps, get_exif_loads, convert_degress_to_decimal)

# AWS_STORAGE_BUCKET_NAME = 'shellcatch'
# AWS_S3_CUSTOM_DOMAIN = 'https://{0:s}.s3.amazonaws.com/'.format(str(AWS_STORAGE_BUCKET_NAME))
# AWS_ACCESS_KEY_ID = 'AKIAJRA5Z7OCTBF7JPNA'
# AWS_SECRET_ACCESS_KEY = '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'
#
#
# def get_connection_bucket():
#     con = boto.connect_s3(
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         calling_format=boto.s3.connection.OrdinaryCallingFormat(),
#     )
#     return con


# def generated_geometry(create_trip_, image_directory, result_dict, path_dst):
#     date_string = str(create_trip_['datetime'].date())
#     if date_string not in result_dict.keys():
#         result_dict[date_string] = dict(date='', mac_address='', geometry=list())
#     result_dict[date_string]['mac_address'] = str(image_directory.split('_')[0])
#     result_dict[date_string]['date'] = date_string
#     result_dict[date_string]['geometry'].append(
#         dict(
#             longitude=str(create_trip_['longitude']),
#             latitude=str(create_trip_['latitude']),
#             image_filepath=path_dst,
#             datetime=str(create_trip_['datetime'])
#         )
#     )
#     return result_dict


# def get_temp_list_folder():
#     conn = get_connection_bucket()
#     bucket_src = conn.get_bucket('shellcatch')
#     src = 'media/uploads/container/temp/'
#     folders = bucket_src.list(prefix=src, delimiter='/')
#     result_list = list()
#     for k in folders:
#         name = k.name.split("/")[-2]
#         result_list.append(name)
#     new_result = result_list[1:]
#
#     result_dict = dict()
#     for i in new_result:
#         directory = str(i)
#         mac_address = directory.split("_")[0]
#         date = directory.split("_")[1]
#         src = "{0}/{1}".format(str('media/uploads/container/temp'), str(i))
#         folders = bucket_src.list(prefix=src)
#         for k in folders:
#             extension_correct = k.name.endswith(('.jpg', '.jpeg'))
#             if extension_correct:
#                 image_name = k.name.split("/")[-1]
#                 if i not in result_dict.keys():
#                     result_dict[i] = dict(directory='', mac_address='', date='', image_name=list())
#                 result_dict[i]['directory'] = directory
#                 result_dict[i]['mac_address'] = mac_address
#                 result_dict[i]['date'] = date
#                 result_dict[i]['image_name'].append(image_name)
#     result = dict(dict_folder=result_dict, bucket_src=bucket_src)
#     return result


# def load_image():
#     conn = get_connection_bucket()
#     bucket_src = conn.get_bucket('shellcatch')
#     src = 'media/uploads/container/temp/'
#     dst = 'media/uploads/container'
#     folders = bucket_src.list(prefix=src, delimiter='.jpg')
#     result_dict = dict()
#     geometry = dict()
#     # i = 0
#     for k in folders:
#         # i += 1
#         extension_correct = k.name.endswith(('.jpg', '.jpeg'))
#         if extension_correct:
#             image_name = k.name.split("/")[-1]
#             image_directory = k.name.split("/")[-2]
#             path_dst = "{0}/{1}/{2}".format(str(dst), str(image_directory), str(image_name))
#             name = k.name
#             # push database
#             create_trip_ = create_trip(name, path_dst)
#             geometry = generated_geometry(create_trip_, image_directory, result_dict, path_dst)
#
#             bucket_src.lookup(k.name)
#             bucket_src.copy_key(path_dst, bucket_src.name, k.name)
#             bucket_src.delete_key(k.name)
#             # if i == 4:
#             #     break
#
#     if geometry:
#         create_json_file(geometry)
#         create_file_csv(geometry)

    # return str('Successfull')

#
# if __name__ == "__main__":
#     get_temp_list_folder()
