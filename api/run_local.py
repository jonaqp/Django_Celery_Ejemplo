from time import time

from api.tasks import (get_temp_list_folder, task_create_json_file, create_trip,
                       task_create_file_csv, task_move_parent_directory)
from api.utils.connection import get_connection_bucket


def run_folder():
    print("Task Get all folder s3: result = %s" % str(time()))
    conn = get_connection_bucket()
    bucket_src = conn.get_bucket('shellcatch')
    temp_list = get_temp_list_folder(bucket_src)
    list_folder = temp_list['folder_list']

    print("Task Finish Get all folder s3: result = %s" % str(time()))

    print("Task Create Trip: result = %s" % str(time()))
    print(list_folder)
    create_trip.delay(list_folder)

    print("Task Create Json: result = %s" % str(time()))
    task_create_json_file.delay(list_folder, bucket_src)

    print("Task Create Csv result = %s" % str(time()))
    task_create_file_csv.delay(list_folder, bucket_src)

    print("Task Move parent folder: result = %s" % str(time()))
    task_move_parent_directory(list_folder, bucket_src)

    print("Task finished: result = %s" % str(time()))


if __name__ == '__main__':
    run_folder()
