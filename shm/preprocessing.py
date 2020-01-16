'''
Task@Jiawei

Let ${Image} := ./clip_img/
Let ${Mask}  := ./matting/

Move ${Images} to ./data/image.
Move ${Mask}   to ./data/mask.
Generate ./data/train.txt.

'''

import pandas as pd
import os
import shutil
from pathlib import Path

def suffix_get(path, suf):
    files = []
    for file in Path(path).rglob('*.'+suf):
        files.append(os.path.join(path, file.name))
    return files

def move_file_to(src_list, aim_dir):
    for file in src_list:
        shutil.move(file, os.path.join(aim_dir, os.path.split(file)[-1]))

def gen_name_list(src_list, where):
    str_ = ''
    for f in src_list:
        str_ += os.path.split(f)[-1].split('.')[0]
        str_ += '\n'
    file = open(where, 'w')
    file.write(str_)
    file.close()


if __name__ == '__main__':
    impath = './clip_img/'
    mapath = './matting/'

    imlist = suffix_get(impath, 'jpg')
    move_file_to(imlist, './Semantic_Human_Matting/data/image')

    malist = suffix_get(mapath, 'jpg')
    move_file_to(malist, './Semantic_Human_Matting/data/mask')

    gen_name_list(imlist, './Semantic_Human_Matting/data/train.txt')