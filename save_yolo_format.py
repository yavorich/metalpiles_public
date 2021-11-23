import sys
import os
import glob
import argparse
import shutil
import base64
import json
import cv2
import numpy as np


id_list = ['valid_metal', 'no_metal', 'long_metal', 'thick_metal',
           'grapple', 'truck', 'magnet']
id_dict = {name: i for i, name in enumerate(id_list)}


def b64_to_img(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
        img = data['imageData']
        img = base64.b64decode(img)
        img = np.frombuffer(img, dtype = np.uint8)
        img = cv2.imdecode(img, 1)
        return img

# def save_img(img_path, img):
    # cv2.imwrite(impg_path, image)
    
    
def save_yolo_file(labels, video_name, frame_name,  save_dir):
    txt_path = os.path.join(frame_name + f'({video_name})' + '.txt')
    txt_path = os.path.join(save_dir, txt_path)
    
    if labels:
        with open(txt_path,'w') as f:
            f.write('\n'.join(labels))
    else:
         print(f'{frame_name}.json doesn\'t have bounding boxes. Please, check this file.')
        
# def save_jpg_file(frame_path, video_name,  save_dir):
    # fn = os.path.basename(frame_path).split('.')[0] + f'({video_name})' + '.jpg' 
    # fn = os.path.basename(frame_path).split('.')[0] + f'({video_name})' + '.json' 
    # print(frame_path)
    # new_path = os.path.join(save_dir, fn)
    # shutil.copy(frame_path,  new_path)
    # img = b64_to_img(frame_path)
    # cv2.imwrite(new_path, img)

def save_jpg_file(img, frame_path, video_name,  save_dir):
    fn = os.path.basename(frame_path).split('.')[0] + f'({video_name})' + '.jpg' 
    # fn = os.path.basename(frame_path).split('.')[0] + f'({video_name})' + '.json' 
    # print(frame_path)
    new_path = os.path.join(save_dir, fn)
    # shutil.copy(frame_path,  new_path)
    # img = b64_to_img(frame_path)
    cv2.imwrite(new_path, img)



def create_yolo_files(frames_path, video_name, save_dir):
    for json_path in glob.glob(os.path.join(frames_path, '*.json')):
        with open(json_path) as f:
            data_str = f.read()
            if '{' in data_str:
                data = json.loads(data_str)
            else:
                print(f'{json_path} is empty. Please, check this file.')
            
        ports_list = []
        
        img = data['imageData']
        if not img:
            print(f'{json_path} has no img data. Please, check this file.')
            continue
        img = base64.b64decode(img)
        img = np.frombuffer(img, dtype = np.uint8)
        img = cv2.imdecode(img, 1)
        
        for i in range(len(data['shapes'])):
            ports_location = data['shapes'][i]['points']
            ports_list.append(ports_location)
        
        frame_path = json_path.split('.')[0] + '.jpg'
        frame_name = os.path.basename(json_path).split('.')[0]
        # save_jpg_file(frame_path, video_name, save_dir)
        save_jpg_file(img, frame_path, video_name, save_dir)
        labels = []
        for i in range(len(data['shapes'])):
            x_lists=[]
            y_lists=[]
            obj_ports = ports_list[i]
            for port in obj_ports:
                x_lists.append(port[0])
                y_lists.append(port[1])
            x_max = sorted(x_lists)[-1]
            x_min = sorted(x_lists)[0]
            y_max = sorted(y_lists)[-1]
            y_min = sorted(y_lists)[0]

            width = x_max-x_min
            height = y_max-y_min
            
            # u,v,_ = cv2.imread(frame_path).shape
            u,v,_ = img.shape
            
                
            center_x,center_y = round(float((x_min+width/2.0)/v),6),round(float((y_min+height/2.0)/u),6)
            
            f_width,f_height = round(float(width/v),6),round(float(height/u),6)
            
            label_id = str(id_dict[data['shapes'][i]['label']])
            
            labels.append(label_id+' '+str(center_x)+' '+str(center_y)+' '+str(f_width)+' '+str(f_height))
            
        save_yolo_file(labels,
                           video_name, frame_name, save_dir)
    # print('Сonversion to yolo format completed')
    
def create_train_file(data_dir, save_dir):
    train_fn = 'train.txt'
    
    labels_list = glob.glob(os.path.join(data_dir, '*.jpg'))
    train_paths_list = []
    
#     if data_dir.split(os.path.sep)[-1]!='data':
#         raise ValueError('root directory should be \'data\'')
    
    for labels_path in labels_list:
        fn = os.path.basename(labels_path)
        jpg_fn = fn.split('.')[0] + '.jpg'
        data_path = os.path.join('data', jpg_fn)
        
        train_paths_list.append(data_path)
    
    with open(os.path.join(save_dir, train_fn), 'w') as f:
        f.write('\n'.join(train_paths_list))
    
def parseArguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',type=str,
                        help='the path of the dataset')
    parser.add_argument('--save_dir', type = str, help = 'the path where files will be saved')
    
    return parser.parse_args(argv)    
    
def main(args):
    data_dir = args.data_dir
    save_dir = args.save_dir
    videos_list = glob.glob(os.path.join(data_dir, '*'))
    for frames_path in videos_list:
        video_name = os.path.basename(frames_path)
        create_yolo_files(frames_path, video_name, save_dir)
        print(f'{video_name} frames saved')
    create_train_file(data_dir = save_dir, save_dir = save_dir)
    print(f'All frames saved to {save_dir}')
    
    
if __name__=='__main__':
   main(parseArguments(sys.argv[1:]))