import cv2
import shutil
from numpy import *

from PIL import Image
import os
import re
import pytesseract


gl_file_list_jpg = []
gl_list_photo2word = []# 最终list


def get_frame_from_video(video_name, time_interval):
    
    cap = cv2.VideoCapture(video_name)
    frames_fps = cap.get(5)  # 帧率  CAP_PROP_FPS
    print(frames_fps)
    frames_num = cap.get(7)  # 帧数  CAP_PROP_FRAME_COUNT
    interval = int(frames_fps * time_interval / 1000)


    # 保存图片的路径
    save_path = video_name.split('.mp4')[0]

    # 判断路径是否存在
    is_exists = os.path.exists(save_path)
    if not is_exists:  # 路径不存在
        os.makedirs(save_path)  # 创建路径
        print('path of %s is built' % save_path)
    else:  # 路径存在
        shutil.rmtree(save_path)  # 重新建立文件夹
        os.makedirs(save_path)
        print('path of %s already exist and is rebuilt' % save_path)

    position = arange(1, frames_num, interval)  # 指定抽取的帧，生成数列
    capture = cv2.VideoCapture(video_name)

    j = 0  # 图片序号

    for i in position:

        capture.set(propId=cv2.CAP_PROP_POS_FRAMES, value=i)  # 跳到指定帧
        has_frame, frame = capture.read()
        if has_frame:
            # 保存图片
            save_name = save_path +'\\' +save_path.split('\\')[len(save_path.split('\\'))-1] + '_' + str(j) + '_' + str(time_interval*j) + '.jpg'
            print(save_path)
            print(save_name)
            j += 1
            
            cv2.imencode('.jpg', frame)[1].tofile(save_name) 

        if not has_frame:
            print('video is all read')
            break

def getFilesPath_jpg(path):
    # 获得指定目录中的内容,jpg格式
    file_list = os.listdir(path)
    for file_name in file_list:
        new_path = os.path.join(path, file_name) 
        if os.path.isdir(new_path): 
            getFilesPath_jpg(new_path)
        elif os.path.isfile(new_path):                      
            result = re.match(r".+\.(jpg)$", new_path)
            if result:
                gl_file_list_jpg.append(new_path)                           
        else:
            print("It's not a directory or a file.")


def getwords_fromphotos(file_list):
# 图片转文字
    for images in file_list:
        print(images)
        
        subname = images.split('.')[0]
        n_order = subname.split('_')[len(subname.split('_'))-2]  # 序号 test1-22-15000
        time = subname.split('_')[len(subname.split('_'))-1]    # 起始时间
        text = pytesseract.image_to_string(images, lang='chi_sim')
        gl_list_photo2word.append([time, text])
    print(gl_list_photo2word)


if __name__ == '__main__':
    # 视频文件名字
    video_name = 'test\\voices\\test1.mp4'
    jpg_path = "test\\voices"
    interval = 20000  #间隔（毫秒）
    get_frame_from_video(video_name, interval)# 视频抽帧

    #图片处理
    getFilesPath_jpg(jpg_path)
    getwords_fromphotos(gl_file_list_jpg)
