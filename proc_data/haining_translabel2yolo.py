# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2020/8/27 10:48
# @Author : liumin
# @File : translabel2yolo.py
import copy
import os
import cv2
import re

pattens = ['name', 'xmin', 'ymin', 'xmax', 'ymax']

def get_annotations(xml_path):
    bbox = []
    with open(xml_path, 'r') as f:
        text = f.read().replace('\n', 'return')
        p1 = re.compile(r'(?<=<object>)(.*?)(?=</object>)')
        result = p1.findall(text)
        for obj in result:
            tmp = []
            for patten in pattens:
                p = re.compile(r'(?<=<{}>)(.*?)(?=</{}>)'.format(patten, patten))
                if patten == 'name':
                    tmp.append(p.findall(obj)[0])
                else:
                    tmp.append(int(float(p.findall(obj)[0])))
            bbox.append(tmp)

        p1w = re.compile(r'(?<=<width>)(.*?)(?=</width>)')
        result_w = p1w.findall(text)[0]
        p1h = re.compile(r'(?<=<height>)(.*?)(?=</height>)')
        result_h = p1w.findall(text)[0]
    return bbox, int(result_h), int(result_w)

lbls = {'cell':0, 'barcode':1, 'bigyiwu':2} # {'cell':0,'chuan':1,'pian':2}

rootpath = '/home/lmin/data/BigCut_hn3'
file = open(rootpath+'/img_list.txt')
lines = file.readlines()#读取全部内容
for line in lines:
    imgpath,xmlpath = line.strip().split(' ')
    print(imgpath,xmlpath)
    image = cv2.imread(os.path.join(rootpath,'images/train2017',imgpath))
    gheight,gwidth,_ = image.shape
    bbox,gheight1,gwidth1  = get_annotations(os.path.join(rootpath,'annotations/train2017',xmlpath))

    seg_txt = open(rootpath+'/labels/train2017/' + xmlpath[:-4]+'.txt', 'a+')
    for bb in bbox:
        cls = str(lbls[bb[0]])
        x_center  = str((bb[1]+ bb[3])*0.5/gwidth)
        y_center  = str((bb[2]+ bb[4])*0.5/gheight)
        width  = str((bb[3]- bb[1])*1.0/gwidth)
        height =  str((bb[4]- bb[2])*1.0/gheight)
        seg_txt.write(cls+' '+ x_center + ' ' + y_center + ' ' +width + ' ' + height + '\n')
    seg_txt.close()

file.close()
