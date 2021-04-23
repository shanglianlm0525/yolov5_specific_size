# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021/2/18 15:12
# @Author : liumin
# @File : procCellData_hn3.py

import os
import sys
import cv2
import re
import shutil
from glob2 import glob

defect_cls = 'all_hn3'


def moveValidData():
    root_path = '/home/lmin/data/collections/' + defect_cls + '/'

    '''
    txt_path = os.path.join(root_path, 'img_list.txt')
    if os.path.isfile(txt_path):
        os.remove(txt_path)
    seg_txt = open(txt_path, 'a')
    '''

    org_path = os.path.join(root_path,'org')
    img_path = os.path.join(root_path,'images/train2017')
    xml_path = os.path.join(root_path,'annotations/train2017')
    for dirname in os.listdir(os.path.join(root_path,'org')):
        print(dirname)
        imglist = glob(os.path.join(org_path, dirname, '*.jpg'))
        xmllist = glob(os.path.join(org_path, dirname, '*.xml'))
        for imgPath in imglist:
            # print(imgPath)
            imgname = os.path.basename(imgPath)
            xmlname = imgname.replace('.jpg', '.xml')
            xmlPath = os.path.join(org_path, dirname, xmlname)
            if len(imgname.strip().split(' '))>1:
                continue
            if xmlPath in xmllist:
                print(imgPath,xmlPath)
                shutil.copyfile(imgPath, os.path.join(img_path,imgname))
                shutil.copyfile(xmlPath, os.path.join(xml_path,xmlname))

                # seg_txt.write(imgname + ' ' + imgname.replace('jpg', 'xml') + '\n')
    # seg_txt.close()


def produceImgAndLabelsList():
    root_path = '/home/lmin/data/collections/'+defect_cls+'/'
    seg_txt = open(root_path + 'img_list.txt', 'a')
    imglist = glob(root_path + "images/train2017/*.jpg")
    xml_dir = root_path+'annotations/train2017/'
    xmlpaths = glob(os.path.join(xml_dir, '*.xml'))
    for i, imgPath in enumerate(imglist):
        print(i, imgPath)
        imgname = os.path.basename(imgPath)
        spp = imgname.strip().split(' ')
        if len(spp) >1:
            continue
        xmlname = imgname.replace('.jpg', '.xml')
        if os.path.join(xml_dir, xmlname) in xmlpaths:
            seg_txt.write(imgname+' '+imgname.replace('jpg','xml') + '\n')
    seg_txt.close()


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
    return bbox

lbls = {'handaipianyi': 0, 'yiwu': 1, 'quejiao': 2, 'handailianjie':3, 'handaiqueshi':4, 'handaichaochuhuiliutiao':5 }


def transVoc2Yolo():
    lbl_num = [0] * len(lbls)

    rootpath = '/home/lmin/data/collections/' + defect_cls
    file = open(rootpath + '/img_list.txt')
    lines = file.readlines()  # 读取全部内容
    for line in lines:
        imgpath, xmlpath = line.strip().split(' ')
        print(imgpath, xmlpath)
        image = cv2.imread(os.path.join(rootpath, 'images/train2017', imgpath))
        gheight, gwidth, _ = image.shape
        bbox = get_annotations(os.path.join(rootpath, 'annotations/train2017', xmlpath))

        seg_txt = open(rootpath + '/labels/train2017/' + imgpath[:-4] + '.txt', 'a')
        for bb in bbox:
            if bb[0] not in lbls:
                continue
            cls = str(lbls[bb[0]])
            lbl_num[int(cls)] = lbl_num[int(cls)] + 1
            x_center = str((bb[1] + bb[3]) * 0.5 / gwidth)
            y_center = str((bb[2] + bb[4]) * 0.5 / gheight)
            width = str((bb[3] - bb[1]) * 1.0 / gwidth)
            height = str((bb[4] - bb[2]) * 1.0 / gheight)
            seg_txt.write(cls + ' ' + x_center + ' ' + y_center + ' ' + width + ' ' + height + '\n')
        seg_txt.close()

    file.close()

    print(lbl_num)

## [3752, 6900, 952, 252, 10194, 5226]
moveValidData()
produceImgAndLabelsList()
transVoc2Yolo()

