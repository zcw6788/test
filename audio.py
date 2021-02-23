from moviepy.editor import *
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import os   
import re
import subprocess
import subprocess
import speech_recognition as sr
from aip import AipSpeech

APP_ID = '23671526'
API_KEY = 'ut8NLiolojaLoGSALxqTQ0yv'
SECRET_KEY = 'UN4aVCcSo7suVMmHgqXpQ2qg5tbuh2nL'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# path = 'test\\voices' 


gl_file_list_pcm = []
gl_failed_list = []
gl_file_list_wav = []

time_list = []


def vedio2audio(mp4_path):
    
    video = VideoFileClip(mp4_path)
    audio = video.audio
    wav_ = mp4_path.split('.')[0] + '.wav'
    print(wav_)
    
    audio.write_audiofile(wav_)

# ___________________vedio2audio_______________________________


def cutaudio(wav_path):

    audio = AudioSegment.from_file(wav_path, "wav")
    size = 15000  #切割的毫秒数 10s=10000
    chunks = make_chunks(audio, size)  #将文件切割

    for i, chunk in enumerate(chunks):
        #test\\voices\\test1.wav
        newpath = wav_path.split('.')[0]
        chunk_name = newpath+ "-{0}-".format(i)+str(size)+".wav"
        chunk.export(chunk_name, format="wav")



# _____________________________cutaudio___________________________


def getFilesPath(path, type):
    # 获得指定目录中的内容,wav/pcm格式
    file_list = os.listdir(path)
    for file_name in file_list:
        new_path = os.path.join(path, file_name) 
        if os.path.isdir(new_path): 
            getFilesPath(new_path,type)
        elif os.path.isfile(new_path):          
            if type == 'pcm':
                result = re.match(r".+\.(pcm)$", new_path)
                if result:
                    gl_file_list_pcm.append(new_path)
            elif type =='wav':
                result = re.match(r".+\.(wav)$", new_path)
                if result:
                    gl_file_list_wav.append(new_path)                
        else:
            print("It's not a directory or a file.")
 
def fileProcessing(file_list):
    #print("start----------------")
    codePre = "ffmpeg -y  -i "
    
    codeMid = " -acodec pcm_s16le -f s16le -ac 1 -ar 16000 "
    for file_path in file_list:

        subname = file_path.split('.')
        print(subname)
        output_path = subname[0] + ".pcm"   # 处理后的文件路径
        command = codePre + file_path + codeMid + output_path
        file_name = os.path.basename(file_path).split('.')

        try:
            retcode = subprocess.call(command, shell=True)
            if retcode == 0:
                print(file_name[0], "successed------")
            else:
                print(file_name[0], "is failed--------")
        except Exception as e:
            print("Error:", e)
 
    print("---------------End all-----------------")
    print("failed:", gl_failed_list)




#________________________________baidu___________________________________


def listen(file_list):
# 读取文件
    # print(file_list)
    for file_path in file_list:

        subname = file_path.split('.')
        if '-' in file_path:

            n_order = subname[0].split('-')[1]  #序号 test1-22-15000.wav
            interval = subname[0].split('-')[2]    #间隔
            print(n_order,interval)


            with open(file_path, 'rb') as fp:
                voice = fp.read()

            result = client.asr(voice, 'wav', 16000, {'dev_pid': 1537})
            try:
                result_text = result["result"][0]
                time_list.append([int(n_order)*int(interval), result_text])

            except KeyError:
                print("KeyError")
                print(result)
    print(time_list)



if __name__ == "__main__":
    mp4_path = 'test\\voices\\test1.mp4'
    wav_path = 'test\\voices\\test1.wav'
    vedio2audio(mp4_path)
    cutaudio(wav_path)

    file_path = r'test\voices'
    # 将路径下所有wav文件转为pcm格式
    getFilesPath(file_path, 'wav')
    fileProcessing(gl_file_list_wav)

    #baidu
    getFilesPath(path, 'pcm')
    listen(gl_file_list_pcm)

