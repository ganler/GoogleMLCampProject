[TOC]

## ONNX with OpenCV

- OpenCV always conflicts with ONNX opset 9, so we need to convert it to opset 8. [**LINK**](https://github.com/onnx/onnx/blob/master/docs/PythonAPIOverview.md#converting-opset-version-of-an-onnx-model)
- Keras/TF => input layout: NHWC. However, for onnx, NCHW is used by default. Hence, just convert the model to TF format and use `readNetFromTensorFlow`.
- For most cases with ops like `reshape`, you need to simplify the onnx file. [**LINK**](https://github.com/daquexian/onnx-simplifier)
