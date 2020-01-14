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
# print(df_train)   # 14560 rows
# print(df_val)     # 3641 rows

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
          # For Debug Use
          print(path)
          image = cv2.imread(path)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          X_train[i] = image

      for j, mask_id in enumerate(mask_id_list):
          path = os.path.join(mask_path_list[j], mask_id)
          # For Debug Use
          print(path)
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

      for j, mask_id in enumerate(mask_id_list):
          path = os.path.join(mask_path_list[j], mask_id)
          image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
          image = image[:, :, 3]
          image = np.expand_dims(image, axis=-1)
          image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
          Y_train[j] = image
            
      yield X_train, Y_train

train_gen = train_generator()
val_gen = val_generator()

from keras.models import Model, load_model
from keras.layers import Input, UpSampling2D
from keras.layers.core import Dropout, Lambda
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K

import tensorflow as tf

inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

s = Lambda(lambda x: x / 255) (inputs)

c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (s)
c1 = Dropout(0.1) (c1)
c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c1)
p1 = MaxPooling2D((2, 2)) (c1)

c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p1)
c2 = Dropout(0.1) (c2)
c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c2)
p2 = MaxPooling2D((2, 2)) (c2)

c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p2)
c3 = Dropout(0.2) (c3)
c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c3)
p3 = MaxPooling2D((2, 2)) (c3)

c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p3)
c4 = Dropout(0.2) (c4)
c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c4)
p4 = MaxPooling2D(pool_size=(2, 2)) (c4)

c5 = Conv2D(256, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p4)
c5 = Dropout(0.3) (c5)
c5 = Conv2D(256, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c5)

u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same') (c5)
u6 = concatenate([u6, c4])
c6 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u6)
c6 = Dropout(0.2) (c6)
c6 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c6)

u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (c6)
u7 = concatenate([u7, c3])
c7 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u7)
c7 = Dropout(0.2) (c7)
c7 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c7)

u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c7)
u8 = concatenate([u8, c2])
c8 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u8)
c8 = Dropout(0.1) (c8)
c8 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c8)

u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c8)
u9 = concatenate([u9, c1], axis=3)
c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u9)
c9 = Dropout(0.1) (c9)
c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c9)

outputs = Conv2D(1, (1, 1), activation='sigmoid') (c9)

model = Model(inputs=[inputs], outputs=[outputs])

model.compile(optimizer='adam', loss='binary_crossentropy')

num_train_samples = len(df_train)
num_val_samples = len(df_val)
train_batch_size = BATCH_SIZE
val_batch_size = BATCH_SIZE

train_steps = np.ceil(num_train_samples / train_batch_size)
val_steps = np.ceil(num_val_samples / val_batch_size)

filepath = "model.h5"

earlystopper = EarlyStopping(patience=3, verbose=1)

checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, 
                             save_best_only=True, mode='min')

callbacks_list = [earlystopper, checkpoint]

history = model.fit_generator(train_gen, steps_per_epoch=train_steps, epochs=20, 
                                validation_data=val_gen, validation_steps=val_steps, 
                                verbose=1, callbacks=callbacks_list)
