# Lirary
import pandas as pd
import numpy as np
import cv2
import os

from sklearn.model_selection import train_test_split
from skimage.transform import resize

# Constant Parameters
IMG_HEIGHT = 128
IMG_WIDTH = 128
IMG_CHANNELS = 3

BATCH_SIZE = 100

root_path = '../../ml-camp/MattingHuman/aisegmentcom-matting-human-datasets'
clip_root_path = os.path.join(root_path, 'clip_img')
mask_root_path = os.path.join(root_path, 'matting')

df_clip = pd.DataFrame()
# eg. first_folder = 1803151818
# eg. second_folder = clip_00000000
first_folder_list = os.listdir(clip_root_path)
for i, first_folder in enumerate(first_folder_list):
    second_folder_list = os.listdir(os.path.join(clip_root_path, first_folder))
    for j, second_folder in enumerate(second_folder_list):
        image_list = os.listdir(os.path.join(clip_root_path, first_folder, second_folder))
        df_tmp = pd.DataFrame(image_list, columns=['clip_id'])
        df_tmp['clip_path'] = os.path.join(clip_root_path, first_folder, second_folder)
        df_clip = pd.concat([df_clip, df_tmp], axis=0).reset_index(drop=True)
# For Debug Use
# print(df_clip.head())
# print(df_clip.tail())

df_mask = pd.DataFrame()
# eg. first_folder = 1803151818
# eg. second_folder = matting_00000000
first_folder_list = os.listdir(mask_root_path)
for i, first_folder in enumerate(first_folder_list):
    second_folder_list = os.listdir(os.path.join(mask_root_path, first_folder))
    for j, second_folder in enumerate(second_folder_list):
        image_list = os.listdir(os.path.join(mask_root_path, first_folder, second_folder))
        df_tmp = pd.DataFrame(image_list, columns=['mask_id'])
        df_tmp['mask_path'] = os.path.join(clip_root_path, first_folder, second_folder)
        df_mask = pd.concat([df_mask, df_tmp], axis=0).reset_index(drop=True)
# For Debug Use
# print(df_mask.head())
# print(df_mask.tail())

def get_name(img_id):
    name = img_id.split('.')[0]
    return name

df_clip['merge_id'] = df_clip['clip_id'].apply(get_name)
df_mask['merge_id'] = df_mask['mask_id'].apply(get_name)

df_data = pd.merge(df_clip, df_mask, on = 'merge_id')[['clip_id', 'clip_path', 'mask_id', 'mask_path']].reset_index(drop=True)
# For Debug Use
print(df_data.head())
print(df_data.tail())
