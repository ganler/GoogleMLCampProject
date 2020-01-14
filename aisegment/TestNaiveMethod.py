from keras.models import Model, load_model

model = load_model('model.h5')
model.summary()

import pandas as pd
import numpy as np
import cv2
import os

from sklearn.model_selection import train_test_split
from skimage.transform import resize

import matplotlib.pyplot as plt

# Constant Parameters
IMG_HEIGHT = 128
IMG_WIDTH = 128
IMG_CHANNELS = 3

BATCH_SIZE = 500

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
        df_tmp['mask_path'] = os.path.join(mask_root_path, first_folder, second_folder)
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


# For Test Use
SAMPLE_SIZE = 100
df_test = df_data.sample(SAMPLE_SIZE, random_state=0).reset_index(drop=True)
# For Debug Use
print(df_data.head())
print(df_data.tail())

df_test.to_csv('df_test.csv.gz', compression='gzip', index=False)

def test_generator(batch_size=1):
  while True:
    for df in pd.read_csv('df_test.csv.gz', chunksize=batch_size):  
      test_id_list = list(df['clip_id'])
      test_path_list = list(df['clip_path'])

      X_test = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        
      for i, test_id in enumerate(test_id_list):
          path = os.path.join(test_path_list[i], test_id)
          # For Debug Use
          # print(path)
          image = cv2.imread(path)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          X_test[i] = image
            
      yield X_test

test_gen = test_generator()

predictions = model.predict_generator(test_gen, steps=len(df_test), verbose=1)

test_id_list = list(df_test['clip_id'])
for i, test_id in enumerate(test_id_list):
    image = predictions[i]
    image = resize(image, (800, 600))
    image = image.reshape((1, 800, 600, 1))

    if i == 0:
        preds = image
    else:
        preds = np.vstack((preds, image))

alpha_preds = (preds >= 0.5).astype(np.uint8) * 255

X_test = np.zeros((len(df_test), 800, 600, 3), dtype=np.uint8)

test_id_list = list(df_test['clip_id'])
test_path_list = list(df_test['clip_path'])

for i, test_id in enumerate(test_id_list):
        path = os.path.join(test_path_list[i], test_id)
        image = cv2.imread(path)
        image = resize(image, (800, 600), mode='constant', preserve_range=True)
        X_test[i] = image
        
print(X_test.shape)
print(alpha_preds.shape)

predicted_masks = np.concatenate((X_test, alpha_preds), axis=-1)

for i, test_id in enumerate(test_id_list):
        plt.imshow(predicted_masks[i])
        plt.save(test_id)    