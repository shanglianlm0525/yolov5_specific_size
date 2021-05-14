# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021/5/7 16:57
# @Author : liumin
# @File : aug_data.py

import os
import sys
import re
import shutil

import cv2


def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path) and not path.endswith('_aug'):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files

root_path = '/home/lmin/data/collections/all_hn3/org'
_fs = list_all_files(root_path)
#将第一阶段的文件遍历出来
print(len(_fs))

img_list = []
xml_list = []
for i, path in enumerate(_fs):
    if path.endswith('.jpg'):
        img_list.append(path)
    elif path.endswith('.xml'):
        xml_list.append(path)


print(len(img_list), len(xml_list))

for _dir in os.listdir(root_path):
    for i in ['bbox1plus_aug','bbox2plus_aug','bbox3plus_aug','bbox4plus_aug'
        ,'bbox1minus_aug','bbox2minus_aug','bbox3minus_aug','bbox4minus_aug'
        ,'bbox13plus_aug','bbox24plus_aug','bbox13minus_aug','bbox24minus_aug']:
        if not os.path.exists(os.path.join(root_path, _dir+ '_' +str(i))):
            os.mkdir(os.path.join(root_path, _dir+  '_' + str(i)))


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


from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString


def produceXMl(imgname, height, width, smallImgs_offsets):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'PVD'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = imgname

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(width)

    node_height = SubElement(node_size, 'height')
    node_height.text = str(height)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    for offsets in smallImgs_offsets:
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = str(offsets[0])
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(offsets[1])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(offsets[2])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(offsets[3])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(offsets[4])

    xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
    dom = parseString(xml)
    # print(xml)
    return xml

aug_lbls = {'handaipianyi', 'yiwu', 'handailianjie', 'handaiqueshi', 'handaichaochuhuiliutiao' } # 'quejiao',

for img_path, xml_path in zip(sorted(img_list),sorted(xml_list)):
    print(img_path,xml_path)
    dirname = os.path.dirname(img_path)
    if dirname.endswith('_aug'):
        continue
    imgname = os.path.basename(img_path)
    [fname, fsuffix] = imgname.split('.')

    image = cv2.imread(img_path)
    height, width, _ = image.shape
    bbox = get_annotations(xml_path)

    aug_bbox1plus = []
    aug_bbox2plus = []
    aug_bbox3plus = []
    aug_bbox4plus = []
    aug_bbox1minus = []
    aug_bbox2minus = []
    aug_bbox3minus = []
    aug_bbox4minus = []
    aug_bbox13plus = []
    aug_bbox24plus = []
    aug_bbox13minus = []
    aug_bbox24minus = []
    for bb in bbox:
        if bb[0] not in aug_lbls:
            aug_bbox1plus.append(bb)
            aug_bbox2plus.append(bb)
            aug_bbox3plus.append(bb)
            aug_bbox4plus.append(bb)
            aug_bbox1minus.append(bb)
            aug_bbox2minus.append(bb)
            aug_bbox3minus.append(bb)
            aug_bbox4minus.append(bb)
            aug_bbox13plus.append(bb)
            aug_bbox24plus.append(bb)
            aug_bbox13minus.append(bb)
            aug_bbox24minus.append(bb)
            continue
        cls, x1, y1, x2, y2 = bb[0], bb[1], bb[2], bb[3], bb[4]
        aug_bbox1plus.append([bb[0], bb[1]-1, bb[2], bb[3], bb[4]])
        aug_bbox2plus.append([bb[0], bb[1], bb[2]-1, bb[3], bb[4]])
        aug_bbox3plus.append([bb[0], bb[1], bb[2], bb[3]+1, bb[4]])
        aug_bbox4plus.append([bb[0], bb[1], bb[2], bb[3], bb[4]+1])
        if bb[3]-bb[1]<4:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox1minus.append([bb[0], bb[1]+1, bb[2], bb[3], bb[4]])
        if bb[4]-bb[2]<4:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox2minus.append([bb[0], bb[1], bb[2]+1, bb[3], bb[4]])
        if bb[3]-bb[1]<4:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox3minus.append([bb[0], bb[1], bb[2], bb[3]-1, bb[4]])
        if bb[4]-bb[2]<4:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox4minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]-1])
        aug_bbox13plus.append([bb[0], bb[1]-1, bb[2], bb[3]+1, bb[4]])
        aug_bbox24plus.append([bb[0], bb[1], bb[2]-1, bb[3], bb[4]+1])
        if bb[3]-bb[1]<5:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox13minus.append([bb[0], bb[1]+1, bb[2], bb[3]-1, bb[4]])
        if bb[4]-bb[2]<5:
            aug_bbox1minus.append([bb[0], bb[1], bb[2], bb[3], bb[4]])
        else:
            aug_bbox24minus.append([bb[0], bb[1], bb[2]+1, bb[3], bb[4]-1])


    xml = produceXMl(imgname, height, width, aug_bbox1plus)
    save_xml = os.path.join(dirname+'_bbox1plus_aug', fname+'_bbox1plus'+'.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox1plus_aug', fname + '_bbox1plus' + '.jpg')
    shutil.copyfile(img_path, save_img)


    xml = produceXMl(imgname, height, width, aug_bbox2plus)
    save_xml = os.path.join(dirname + '_bbox2plus_aug', fname + '_bbox2plus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox2plus_aug', fname + '_bbox2plus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox3plus)
    save_xml = os.path.join(dirname + '_bbox3plus_aug', fname + '_bbox3plus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox3plus_aug', fname + '_bbox3plus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox4plus)
    save_xml = os.path.join(dirname + '_bbox4plus_aug', fname + '_bbox4plus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox4plus_aug', fname + '_bbox4plus' + '.jpg')
    shutil.copyfile(img_path, save_img)


    xml = produceXMl(imgname, height, width, aug_bbox1minus)
    save_xml = os.path.join(dirname + '_bbox1minus_aug', fname + '_bbox1minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox1minus_aug', fname + '_bbox1minus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox2minus)
    save_xml = os.path.join(dirname + '_bbox2minus_aug', fname + '_bbox2minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox2minus_aug', fname + '_bbox2minus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox3minus)
    save_xml = os.path.join(dirname + '_bbox3minus_aug', fname + '_bbox3minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox3minus_aug', fname + '_bbox3minus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox4minus)
    save_xml = os.path.join(dirname + '_bbox4minus_aug', fname + '_bbox4minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox4minus_aug', fname + '_bbox4minus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox13plus)
    save_xml = os.path.join(dirname + '_bbox13plus_aug', fname + '_bbox13plus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox13plus_aug', fname + '_bbox13plus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox24plus)
    save_xml = os.path.join(dirname + '_bbox24plus_aug', fname + '_bbox24plus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox24plus_aug', fname + '_bbox24plus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox13minus)
    save_xml = os.path.join(dirname + '_bbox13minus_aug', fname + '_bbox13minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox13minus_aug', fname + '_bbox13minus' + '.jpg')
    shutil.copyfile(img_path, save_img)

    xml = produceXMl(imgname, height, width, aug_bbox24minus)
    save_xml = os.path.join(dirname + '_bbox24minus_aug', fname + '_bbox24minus' + '.xml')
    with open(save_xml, 'wb') as f:
        f.write(xml)
    save_img = os.path.join(dirname + '_bbox24minus_aug', fname + '_bbox24minus' + '.jpg')
    shutil.copyfile(img_path, save_img)





'''
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
'''