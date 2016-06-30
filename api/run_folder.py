import datetime as datetimex
from api.tasks import create_trip, get_temp_list_folder


def run_folder():
    temp_list = get_temp_list_folder()
    list_folder = temp_list['folder_list']
    bucket_src = temp_list['bucket_src']
    # dst = 'media/uploads/container'
    print(datetimex.datetime.now())
    create_trip(list_folder)
    # task_create_json_file.delay(list_folder, bucket_src)


if __name__ == "__main__":
    run_folder()
