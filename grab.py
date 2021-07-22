from PIL import ImageGrab
from PIL import BmpImagePlugin
from aip import AipOcr
from win10toast import ToastNotifier

import sys, os
import keyboard
import time, datetime
import random
from os import path

from multiprocessing.dummy import Pool as ThreadPool

PIC_DIR = r"C:\Users\hytian3019\Pictures\ocr"

#百度云账号设置
APP_ID = '18427626'
API_KEY = 'GuE2qgGbvECFxdDDahxeL4Vn'
SECRET_KEY = 'nbrSyUGfsXxnCXhyOZ0nN5N804UoXwAO'
#百度云api对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

toaster = ToastNotifier()

esc_pressed = False
ctrl_prtscr_pressed = False

def print_sep(n = 50):
    print('\n'+ '>' * 50 + '\n')

def ctrl_prtscr_cb():
    global ctrl_prtscr_pressed
    print('- [Ctrl + PrtScr] pressed')
    toaster.show_toast('PyOCR',"[Ctrl + PrtScr] pressed pressed", duration=1.5)
    ctrl_prtscr_pressed = True

def esc_cb():
    global ctrl_prtscr_pressed
    global esc_pressed
    if ctrl_prtscr_pressed:
        print('- [Esc] pressed, skip this hot key.')
        print_sep()
        toaster.show_toast('PyOCR',"[Esc] pressed, skip hot key", duration=1.5)
        esc_pressed = True

keyboard.add_hotkey('esc', esc_cb)
keyboard.add_hotkey('Ctrl+print screen', ctrl_prtscr_cb)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def clip_text(astr):
    os.system(f'echo {astr} | clip')

def ocr_image(pic_path):
    """
    docstring
    """
    image = get_file_content(pic_path)
    options = dict(
        probability = True,
        recognize_granularity = 'small',
        poly_location = True,
    )
    data = client.general(image, options)
    return data

def ocr():
    global ctrl_prtscr_pressed
    global esc_pressed
    esc_pressed = False
    ctrl_prtscr_pressed = False
    print('Waiting for hot key [Ctrl + PrtScr] ...')
    keyboard.wait('Ctrl+print screen')
    while not esc_pressed:
        time.sleep(1)  #等待截图
        im = ImageGrab.grabclipboard()  #获取剪切板中的图片
        if isinstance(im, BmpImagePlugin.DibImageFile):  #若剪切板的内容可以解析成图片
            #print('- Found image on clipboard.')
            #文件名
            ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            rnd = str(random.randint(100, 1000))
            #保存图片
            pic_path = path.join(PIC_DIR, ts + rnd + '.png')
            im.save(pic_path)
            #print('- Saved to ', pic_path)
                        
            data = ocr_image(pic_path)
            #print('- Parsed results: ', data)
            words_result = data['words_result']
            data = []  # 需要保存的内容
            for words in words_result:
                data.append(words['words'])
            
            data = ''.join(data).strip()
            #换成中文标点符号
            data = data.replace(',', '，')
            data = data.replace(':', '：')
            data = data.replace(';', '；')
            data = data.replace('(', '（')
            data = data.replace(')', '）')

            print('- OCR result: ', data)
            #print('Put text on clipboard.')
            print_sep()
            clip_text(data)
            toaster.show_toast('PyOCR', data, duration=1.5)
            break

if __name__ == "__main__":
    #ocr()
    #clip_text('好的让我')
    #toaster.show_toast('PyOCR',"Hot key pressed", duration=2)
    print(ocr_image(r'c:\temp\ocr.png'))