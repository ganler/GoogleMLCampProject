import keras
import keras2onnx
import onnx

from keras.models import load_model

model = load_model('./model.h5')
onnx_model = keras2onnx.convert_keras(model, model.name)
onnx.save_model(onnx_model, './model.onnx')
