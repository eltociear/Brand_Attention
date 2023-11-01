import torch
import cv2
import numpy as np
from torchvision import transforms, utils, models
from saliency_prediction.utils.data_process import preprocess_img, postprocess_img
from saliency_prediction.model import TranSalNet


def saliency_map_prection(img_path , text_map_path , weight_path , output_path):

    # Set Device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # load Model
    model = TranSalNet()
    model.load_state_dict(torch.load(weight_path))
    model = model.to(device)
    model.eval()
    print("Model loaded...")

    img = preprocess_img(img_path)
    name = img_path.split('/')[-1].split('.')[0]
    tmap = preprocess_img(text_map_path)

    img = np.array(img) / 255.
    tmap = np.array(tmap) / 255.

    img = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)
    tmap = np.expand_dims(np.transpose(tmap, (2, 0, 1)), axis=0)

    img = torch.from_numpy(img)
    tmap = torch.from_numpy(tmap)

    img = img.type(torch.cuda.FloatTensor).to(device)
    tmap = tmap.type(torch.cuda.FloatTensor).to(device)

    pred_saliency = model(img, tmap)
    toPIL = transforms.ToPILImage()
    pic = toPIL(pred_saliency.squeeze())
    pred_saliency = postprocess_img(pic, img_path)

    cv2.imwrite(output_path + "/" + name + '_saliency_map.png', pred_saliency, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # save the result
    print('Finished')

