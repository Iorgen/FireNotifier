from fastai.vision import *  # import the vision module
from fastai.metrics import error_rate  # import our evaluation metric
import zipfile # import module to unzip the data
import urllib.request
import os # import module to access file paths
from fastai.data.transforms import trace
from fastai.vision.all import *
from pathlib import Path


# url = 'http://madm.dfki.de/files/sentinel/EuroSAT.zip'
# urllib.request.urlretrieve(url,"2750.zip")
# zf = zipfile.ZipFile("2750.zip")
# zf.extractall()
data_path = os.getcwd()
# path = os.path.join(data_path, '2750')
path = Path(data_path+'/2750')

dls = ImageDataLoaders.from_folder(path, valid_pct=0.2,  valid='val',
                                   item_tfms=RandomResizedCrop(128, min_scale=0.35),
                                   batch_tfms=Normalize.from_stats(*imagenet_stats))

dls.show_batch()
learn = cnn_learner(dls, resnet50, metrics=error_rate)
lr = 3.63E-03
learn.fit_one_cycle(6, slice(lr))
learn.export('resnet50_mod_01.pkl')
# learn = create_cnn(data, models.resnet50, metrics=error_rate)
# print(learn.summary())