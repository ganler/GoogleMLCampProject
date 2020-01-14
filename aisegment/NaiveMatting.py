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
# print(df_data.head())
# print(df_data.tail())

df_train, df_val = train_test_split(df_data, test_size=0.2, random_state=0)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)

# For Debug Use
# print(df_train)
# print(df_val)

df_train.to_csv('df_train.csv.gz', compression='gzip', index=False)
df_val.to_csv('df_val.csv.gz', compression='gzip', index=False)

def train_generator(batch_size=100):
  while True:
    for df in pd.read_csv('df_train.csv.gz', chunksize=batch_size):  
      clip_id_list = list(df['clip_id'])
      clip_path_list = list(df['clip_path'])
      mask_id_list = list(df['mask_id'])
      mask_path_list = list(df['mask_path'])

      X_train = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
      Y_train = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
        
      for i, clip_id in enumerate(clip_id_list):
          path = os.path.join(clip_path_list[i], clip_id)
          image = cv2.imread(path)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          X_train[i] = image

      for j, mask_id in enumerate(mask_path_list):
          path = os.path.join(mask_path_list[i], mask_id)
          image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
          image = image[:, :, 3]
          image = np.expand_dims(image, axis=-1)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          Y_train[j] = image
            
      yield X_train, Y_train

def val_generator(batch_size=100):
  while True:
    for df in pd.read_csv('df_train.csv.gz', chunksize=batch_size):  
      clip_id_list = list(df['clip_id'])
      clip_path_list = list(df['clip_path'])
      mask_id_list = list(df['mask_id'])
      mask_path_list = list(df['mask_path'])

      X_train = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
      Y_train = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
        
      for i, clip_id in enumerate(clip_id_list):
          path = os.path.join(clip_path_list[i], clip_id)
          image = cv2.imread(path)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          X_train[i] = image

      for j, mask_id in enumerate(mask_path_list):
          path = os.path.join(mask_path_list[i], mask_id)
          image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
          image = image[:, :, 3]
          image = np.expand_dims(image, axis=-1)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          Y_train[j] = image
            
      yield X_train, Y_train

train_gen = train_generator()
val_gen = val_generator()

