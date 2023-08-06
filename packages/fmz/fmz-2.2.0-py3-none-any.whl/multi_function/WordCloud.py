# encoding = utf-8

from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba
import re
import os

directory = (os.path.split(os.path.realpath(__file__))[0]).split("\\")
directory = "/".join(directory)+"/"

def wcloud(text: str, filename: str, img=None):
    try:
        if img is not None:
            image1 = Image.open(img)
            MASK = np.array(image1)
            WC = WordCloud(font_path = directory+"font/simfang.ttf",max_words=2000, height= 400, width=400,mask = MASK, background_color=None, repeat=False,mode='RGBA')
            st1 = re.sub('[，。、“”‘ ’]','',str(text))
            conten = ' '.join(jieba.lcut(st1))
            con = WC.generate(conten)
            con.to_file(filename)
        else:
            WC = WordCloud(font_path = directory+"font/simfang.ttf",max_words=2000, height= 400, width=400, background_color='white',repeat=False,mode='RGBA')
            st1 = re.sub('[，。、“”‘ ’]','',str(text))
            conten = ' '.join(jieba.lcut(st1))
            con = WC.generate(conten)
            con.to_file(filename)
    except:
        return False