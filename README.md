# GoogleMLCampProject
Image Filter: project for 2020 Google ML winter camp.

Group: Social Eggs

## Poster

![poster](poster.png)

## Web Application 

We provide a web application for online style transferring.

### Demo
 ![web2](images/web1.png)

![web1](images/web2.png)

### Setup
Frontend 
(./web-app/src/transfer)

1. install nvm ([Node Version Manager](https://github.com/nvm-sh/nvm))
2. install node.js: nvm install 10.7.0
3. install nrm: npm install -g nrm
4. optional -- switch to taobao mirror: nrm use taobao
4. run demo: npm install && npm run dev
5. produce environment: npm run build && PORT=8080 npm run start

Backend 
(./web-app/src/master_server, ./web-app/src/gpu_server)
1. install Anaconda Python >= 3.6 and Pytorch >= 0.4.1
2. install pynvml: pip install nvidia-ml-py3
3. install Flask-Cors: pip install flask_cors
4. run master_server.py on web server
5. run gpu_server.py and gpu_scheduler.py on GPU server

Note: The default port for master_server.py, gpu_server.py and gpu_scheduler.py are set to 2333, 6666 and 2048. Please change them if any collision.

## Offline Training
Models are trained offline to increase the response rate.

### Matting  [README.md](README.md) 
(./web-app/src/matting-unet）
We first apply matting on the [Matting Human Dataset](https://www.kaggle.com/laurentmih/aisegmentcom-matting-human-datasets).

### Image Style Transfer 
(./web-app/src/torch_training @ ec10eee)

## Face Mask 
(./web-app/src/on-device-inference)
Matting above is based on dataset contains half-body for people, thus not performing well enough to transfer photos with mainly faces. 
To adress this issue, we develop a Key Point Mehod for face mask only. (We can collect a dataset with face matting and train it in the future)

## Results

### BodyMask

#### Pasting

![idnie_out](images/body-mask-transfer/pasting/idnie_out.jpg)

![mosaic_out](images/body-mask-transfer/pasting/mosaic_out.jpg)

#### Seamless-clone

![candy_out](images/body-mask-transfer/seamless-clone/candy_out.jpg)

![mosaic_out](images/body-mask-transfer/seamless-clone/mosaic_out.jpg)

### FaceMask

![udnie.onnxout](images/face-mask-transfer/udnie.onnxout.png)

![candy.onnxout](images/face-mask-transfer/candy.onnxout.png)

### Style-Only

![candy_out](images/style-only/candy_out.jpg)

![idnie_out](images/style-only/idnie_out.jpg)

![mosaic_out](images/style-only/mosaic_out.jpg)

![pointilism_out](images/style-only/pointilism_out.jpg)

![rain_princess_out](images/style-only/rain_princess_out.jpg)

![simpson_out](images/style-only/simpson_out.jpg)