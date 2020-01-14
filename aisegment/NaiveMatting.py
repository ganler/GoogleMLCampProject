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
clip_root_path = os.path.join(root_path + 'clip_img')
matting_root_path = os.path.join(root_path + 'matting')

df_clip = pd.DataFrame()
# eg. first_folder = 1803151818
# eg. second_folder = clip_00000000
first_folder_list = os.listdir(clip_root_path)
for i, first_folder in enumerate(first_folder_list):
    second_folder_list = os.listdir(os.path.join(clip_root_path + first_folder))
    for j, second_folder in enumerate(second_folder_list):
        image_list = os.listdir(os.path.join(clip_root_path + first_folder + second_folder))
        df_tmp = pd.DataFrame(image_list, columns=['clip_id'])
        df_tmp['clip_path'] = os.path.join(clip_root_path + first_folder + second_folder)
        df_clip = pd.concat([df_clip, df_tmp], axis=0).reset_index(drop=True)
print(df_clip.head())
print(df_clip.tail())