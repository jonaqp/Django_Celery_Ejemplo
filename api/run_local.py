from api.tasks import (get_temp_list_folder, task_create_json_file, create_trip,
                       task_create_file_csv, task_move_parent_directory)
from api.utils.connection import get_connection_bucket


def run_folder():

    conn = get_connection_bucket()
    bucket_src = conn.get_bucket('shellcatch')
    temp_list = get_temp_list_folder(bucket_src)
    list_folder = temp_list['folder_list']
    create_trip(list_folder)
    task_create_json_file(list_folder, bucket_src)
    task_create_file_csv(list_folder, bucket_src)
    task_move_parent_directory(list_folder, bucket_src)

if __name__ == '__main__':
    run_folder()
