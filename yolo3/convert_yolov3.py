import xml.etree.ElementTree as ET
import os,shutil

data_path='/Users/markdana/Desktop/VOC2007'
coco_path='/Users/markdana/Downloads/yolo3/data/coco'

def getAnnotation(index):
    filename = os.path.join(data_path, 'Annotations', index + '.xml')
    tree = ET.parse(filename)
    objs = tree.findall('object')
    size = tree.find('size')

    dw = 1./int(size.find('width').text)
    dh = 1./int(size.find('height').text)

    annolist=[]
    for ix, obj in enumerate(objs):
        bbox = obj.find('bndbox')
        name = obj.find('name').text

        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        w = int(bbox.find('xmax').text)-xmin
        h = int(bbox.find('ymax').text)-ymin

        x = xmin + w/2.0 #central point
        y = ymin + h/2.0

        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh

        if(name=='trafficcone'):
            annolist.append(' '.join([str(x)for x in[0,x,y,w,h]]))
        else:
            print(index)

    with open(os.path.join(coco_path,'labels','trainval', index + '.txt'),'a') as f:
        f.write('\n'.join(annolist))

if __name__ == '__main__':
    trainval = os.path.join(data_path, 'ImageSets','Main', 'trainval.txt')
    dir_list=[]
    with open(trainval, 'r')as f:
        lines=[x.strip() for x in f.readlines()]
        for line in lines:
            getAnnotation(line)
            src_dir=os.path.join(data_path, 'JPEGImages',line + '.jpg')
            dst_dir=os.path.join(coco_path, 'images','trainval',line + '.jpg')
            shutil.copyfile(src_dir,dst_dir)

            dir_list.append(dst_dir)
    with open(os.path.join(coco_path,'trainval.txt'),'a')as f:
        f.write('\n'.join(dir_list))
