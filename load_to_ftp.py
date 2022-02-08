import ftplib
import io
import os
import json


def load_to_ftp(file_path, save_path, user, password, address):
    session = ftplib.FTP(address, user, password)
    print(session.getwelcome())
    print(session.pwd())
    print(session.nlst())
    # session.cwd('C://Users//pmaks')
    # session.cwd('iVMS-4200alarmPicture')
    with open(file_path, 'rb') as f:
        session.storbinary('STOR ' + save_path, f)
        session.quit()


def load_to_ftp_data(label_data, video_dir, frame_name, labelme_user, user, password, address):
    sep = '/'
    # session = ftplib.FTP(address, user, password)
    with ftplib.FTP(address, user, password) as session:
        binary_label_data = json.dumps(label_data, ensure_ascii=False, indent=2)
        binary_label_data = io.BytesIO(binary_label_data.encode('utf-8'))
        # save_path = labelme_user + sep + video_dir

        save_dir_list = [labelme_user, video_dir]
        for dir in save_dir_list:
            if not (dir in session.nlst()):
                session.mkd(dir)
            session.cwd(dir)
        #     print(f'{save_path} added')

        session.storbinary('STOR ' + frame_name + '.json', binary_label_data)
        # session.quit()

# load_to_ftp(os.path.join('data', 'test_data.txt'),
#             'test/test_data.txt',
#             'user33917',
#             'iXtiHRfJQltm',
#             '195.69.187.77')

json_data = {1: 'one', 2: 'two', 3: 'four'}
load_to_ftp_data(json_data,
                 'videos',
                 'frame',
                 'labelme_user',
                 'user33917',
                 'iXtiHRfJQltm',
                 '195.69.187.77')
# session = ftplib.FTP(address, user, password)
# print(session.pwd())
# session.quit()
