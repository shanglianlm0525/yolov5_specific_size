# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021/1/20 18:01
# @Author : liumin
# @File : haining_procData.py


import os
import sys
import re

import shutil


def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files


_fs = list_all_files('/home/lmin/data/BigCut_hn3/org')
#将第一阶段的文件遍历出来
print(len(_fs))

jpg_list = []
xml_list = []
for i, path in enumerate(_fs):
    if path.endswith('.jpg'):
        jpg_list.append(path)
    elif path.endswith('.xml'):
        xml_list.append(path)


print(len(jpg_list), len(xml_list))

root_path = '/home/lmin/data/BigCut_hn3'
new_jpg_path = os.path.join(root_path, 'images/train2017')
new_xml_path = os.path.join(root_path, 'annotations/train2017')

seg_txt = open(root_path + '/img_list.txt', 'a')
for jpg,xml in zip(sorted(jpg_list),sorted(xml_list)):
    jpg2 = os.path.basename(jpg)
    # xml2 = os.path.basename(xml)
    xml2 = jpg2.replace('.jpg', '.xml')

    seg_txt.write(jpg2 + ' ' + xml2 + '\n')

    shutil.copyfile(jpg, os.path.join(new_jpg_path, jpg2))
    shutil.copyfile(xml, os.path.join(new_xml_path, xml2))

seg_txt.close()