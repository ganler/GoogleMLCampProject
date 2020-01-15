import os
import sys
import time
import re

import numpy as np
import torch
from torch import optim, nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms

import utils
from transfer_net import TransferNet
from vgg import Vgg16


class Config:
    seed = 42
    device_id = 0
    epochs = 2
    batch_size = 4
    dataset = './data/train_images/'
    style_image = None
    save_model_path = None
    image_size = 256
    style_size = None
    content_weight = 1e5
    style_weight = 1e10
    lr = 1e-3
    model = None
    content_image = None
    content_scale = None
    output_image = None
    

def check_paths(config):
    try:
        if not os.path.exists(config.save_model_dir):
            os.makedirs(config.save_model_dir)
        if config.checkpoint_model_dir is not None and not (os.path.exists(config.checkpoint_model_dir)):
            os.makedirs(config.checkpoint_model_dir)
    except OSError as e:
        print(e)
        sys.exit(1)    
        
def set_seed(seed):
    np.random.seed(config.seed)
    torch.manual_seed(config.seed)

def train(config):
    device = torch.device('cuda', config.device_id)
    set_seed(config.seed)
    check_paths(config)
    
    transform = transforms.Compose([
        transforms.Resize(config.image_size),
        transforms.CenterCrop(config.image_size),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    train_dataset = datasets.ImageFolder(config.dataset, transform)
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size)

    transfer_net = TransferNet().to(device)
    optimizer = optim.Adam(transfer_net.parameters(), lr=config.lr)
    mse_loss = nn.MSELoss()

    vgg = Vgg16(requires_grad=False).to(device)
    style_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    style = utils.load_image(config.style_image, size=config.style_size)
    style = style_transform(style)
    style = style.repeat(config.batch_size, 1, 1, 1).to(device)

    features_style = vgg(utils.normalize_batch(style))
    gram_style = [utils.gram_matrix(y) for y in features_style]

    for e in range(config.epochs):
        transfer_net.train()
        agg_content_loss = 0.
        agg_style_loss = 0.
        count = 0
        for batch_id, (x, _) in enumerate(train_loader):
            n_batch = len(x)
            count += n_batch
            optimizer.zero_grad()

            x = x.to(device)
            y = transfer_net(x)

            y = utils.normalize_batch(y)
            x = utils.normalize_batch(x)

            features_y = vgg(y)
            features_x = vgg(x)

            content_loss = config.content_weight * mse_loss(features_y.relu2_2, features_x.relu2_2)

            style_loss = 0.
            for ft_y, gm_s in zip(features_y, gram_style):
                gm_y = utils.gram_matrix(ft_y)
                style_loss += mse_loss(gm_y, gm_s[:n_batch, :, :])
            style_loss *= config.style_weight

            total_loss = content_loss + style_loss
            total_loss.backward()
            optimizer.step()

            agg_content_loss += content_loss.item()
            agg_style_loss += style_loss.item()

    transfer_net.eval().cpu()
    save_model_path = config.save_model_path
    torch.save(transfer_net.state_dict(), save_model_path)

    print("\nDone, trained model saved at", save_model_path)


def stylize(config):
    device = torch.device('cuda', config.device_id)

    content_image = utils.load_image(config.content_image, scale=config.content_scale)
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = TransferNet()
        state_dict = torch.load(config.model)
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        
        start = time.time()
        output = style_model(content_image).cpu()
            
    utils.save_image(config.output_image, output[0])
    torch.cuda.empty_cache()
    print('Cost {:.4f}s.'.format(time.time() - start))

    
if __name__ == "__main__":
    config = Config()
    #train(config)
    #stylize(config)
