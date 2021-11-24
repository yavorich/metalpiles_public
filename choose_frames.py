import os
import shutil
import glob
import cv2
import json
from datetime import datetime
import itertools
import random

# def get_random_elements(n, ):

# def choose_frames(video_path, save_dir, frames_number):
#     os.system(f'video-toimg {video_path}')
#     os.path.join(save_dir, dir_name)
#     shutil.move(video_path, save_dir)
#     frames_set = os.listdir(video_path.split('.')[0])
#     frames_set = frames_set.difference(used_frames_set)
#     taken_frames_list = random.sample(frames_set, frames_in_video)


def get_random_dataset(videos_list, save_dir, user_name, db_path, n = 200):
    '''
    Gets n frames from video pathes list
    Args:
        videos_list: (list): list of video pathes
        save_dir (str): save directory
        user_name
        db_path
        n
    '''

    # 1. Define necessary variables
    frames_in_video = n // len(videos_list) # Number of frames from each frames directory
    print(frames_in_video)
    taken_frames_list = []
    date = datetime.today().strftime('%d-%m-%Y')
    remained_frames_number = n - frames_in_video * len(videos_list)
    user_path = os.path.join(save_dir, user_name, date)

    if remained_frames_number != 0:
        raise ValueError(f'{n} frames and {len(videos_list)} videos. This parameters should be dividible. Ability to use any number of videos will be added soon (I hope)')

    # 1. Load database and initialize the corresponding set
    db_condition = os.path.exists(db_path)
    print(db_condition)
    # print(os.stat(db_path).st_size == 0)
    # db_condition = os.stat(db_path).st_size == 0 if db_condition else False
    if db_condition:
        with open(db_path) as f:
            used_frames_dict = f.read()
        db_condition = used_frames_dict.strip().replace(' ', '') if db_condition else False
    print(db_condition)

    if not db_condition:
        print(f'{db_path} is empty or does not exist. Do you want to continue? [y/n]:')
        answer = input()
        if answer!='y':
            return
        else:
            used_frames_dict = dict()
            used_frames_set = set()
    else:
        used_frames_dict = json.loads(used_frames_dict)
        used_frames_set = [frames for dates in used_frames_dict.values() for frames in dates.values()]
        used_frames_set = set(itertools.chain(*used_frames_set))

    # Create directories
    try:
        os.makedirs(user_path)
    except FileExistsError:
        raise FileExistsError(f'File {user_path} already exists. Please check the database.')

    # 2. Take frames from each video
    for video_path in videos_list:
        # TODO: Change the way to get frames_path
        frames_path = video_path[:-4]  # Path to frames directory
        videos_dir = os.path.dirname(frames_path)
        video_name = os.path.basename(frames_path)

        # 2.1. Split the video to frames if it is necessary
        if (not os.path.exists(frames_path)) or len(os.listdir(frames_path)) == 0:
            # TODO: Change the way of the method to unpack video
            os.system(f'video-toimg {video_path}')


        # 2.2. Add not yet used frames to taken_current_frames_set
        frames_set = glob.glob(os.path.join(frames_path, '*.jpg'))
        taken_current_frames_set = set(map(lambda x: os.path.join(video_name, os.path.basename(x)), frames_set))
        taken_current_frames_set = taken_current_frames_set.difference(used_frames_set)
        taken_current_frames_set = random.sample(taken_current_frames_set, frames_in_video)

        # 2.3. Add current taken frames to all taken frames list
        taken_frames_list += taken_current_frames_set

        # 2.4. move taken frames
        os.makedirs(os.path.join(user_path, video_name))
        for taken_frame_path in taken_current_frames_set:
            shutil.copy(os.path.join(videos_dir, taken_frame_path), os.path.join(user_path, video_name))
        # taken_current_frames_set = set(map(lambda x: os.path.basename(x).split('.')[0] + f'({video_name})' + '.jpg', taken_current_frames_set))
        # taken_current_frames_set = set(map(lambda x: os.path.join(video_name, os.path.basename(x)), taken_current_frames_set))



    # For last video take (n - frames_in_video*len(videos_list)) if this difference is positive
    # TODO: Add the ability to use any number of files in video_list
    # remained_frames_number = n - frames_in_video*len(videos_list)
    # if remained_frames_number != 0:
    #     pass


    # 3. Save new data in the database
    if user_name not in used_frames_dict:
        # TODO: Add y/n command
        print(f'New user {user_name} added')
        used_frames_dict[user_name] = dict()
        used_frames_dict[user_name][date] = taken_frames_list
    elif date in used_frames_dict[user_name]:
        # TODO: Change error type
        raise ValueError(
            f'On {date} date data has been already saved. Please check the data of user {user_name} date: {date}.')
    else:
        used_frames_dict[user_name][date] = taken_frames_list
    print(used_frames_dict)
    with open(db_path, 'w') as f:
        json.dump(used_frames_dict, f)

    # 4. The end!!!
    print('That\'s all!!!')


get_random_dataset(
    ['..\\data\\videos\\120211017091131_556.avi',
     '..\\data\\videos\\120211014232602_538.avi',
     '..\\data\\videos\\120211014222255_540.avi',
     '..\\data\\videos\\120211017111449_556.avi'],
    save_dir = '..\\data\\examples\\frames',
    user_name = 'New_Name',
    db_path='..\\data\\examples\\frames\\db.json',
    n = 200
    )

