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

root_path = '~/Fxxk'
clip_root_path = os.path.join(root_path, 'clip_img')
mask_root_path = os.path.join(root_path, 'matting')

image_list = os.listdir(clip_root_path)
df_test = pd.DataFrame(image_list, columns=['clip_id'])
df_test['clip_path'] = clip_root_path

df_test.to_csv('df_test.csv.gz', compression='gzip', index=False)

def test_generator(batch_size=1):
  while True:
    for df in pd.read_csv('df_test.csv.gz', chunksize=batch_size):  
      test_id_list = list(df['clip_id'])
      test_path_list = list(df['clip_path'])

      X_test = np.zeros((len(df), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        
      for i, test_id in enumerate(test_id_list):
          path = os.path.join(test_path_list[i], test_id)
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
        cv2.imwrite(test_id.split('.')[0] + '.png', predicted_masks[i])
