import datetime

from api.tasks import (get_temp_list_folder, task_create_json_file, create_trip,
                       task_create_file_csv, task_move_parent_directory, logger)


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
    logger.info("Task finished: result = %s" % str(now))


if __name__ == '__main__':
    run_folder()
