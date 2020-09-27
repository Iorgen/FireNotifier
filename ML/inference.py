from fastai.vision import *  # import the vision module
from fastai.metrics import error_rate  # import our evaluation metric
import zipfile # import module to unzip the data
import urllib.request
import os # import module to access file paths
from fastai.data.transforms import trace
from fastai.vision.all import *
from fastai.vision import *
from fastai.imports import *

from PIL import Image as PImage
import cv2
from fastai.vision import *
learn = load_learner('./2750/resnet50_mod_01.pkl')
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
pil_im = PImage.fromarray(frame)
x = pil2tensor(pil_im ,np.float32)
preds_num = learn.predict(Image(x))[2].numpy()