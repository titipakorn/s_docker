# Regular python libraries
from utils_cv.similarity.model import compute_features, compute_feature, compute_features_learner
from utils_cv.similarity.metrics import compute_distances, vector_distance
from utils_cv.similarity.plot import plot_distances
from utils_cv.similarity.data import Urls
from utils_cv.common.gpu import which_processor, db_num_workers
from utils_cv.common.data import unzip_url
import math
import os
import random
import sys
import torch
import numpy as np
from pathlib import Path
import torch.nn as nn
from model import NormSoftmaxLoss, EmbeddedFeatureWrapper, L2NormalizedLinearLayer

# Fast.ai
import fastai
from fastai.layers import FlattenedLoss
from fastai.vision import (
    cnn_learner,
    DatasetType,
    ImageList,
    imagenet_stats,
    models,
    open_image
)

# Computer Vision repository

print(f"Fast.ai version = {fastai.__version__}")
which_processor()

# Dataset
data_root_dir = '/app/similarity_data/'
DATA_FINETUNE_PATH = os.path.join(data_root_dir, "train")
DATA_RANKING_PATH = os.path.join(data_root_dir, "test")
print("Image root directory: {}".format(data_root_dir))

# DNN configuration and learning parameters. Use more epochs to possibly improve accuracy.
EPOCHS_HEAD = 12  # 12
EPOCHS_BODY = 12  # 12
HEAD_LEARNING_RATE = 0.01
BODY_LEARNING_RATE = 0.0001
BATCH_SIZE = 32
IM_SIZE = 224
DROPOUT = 0
ARCHITECTURE = models.resnet50

# Desired embedding dimension. Higher dimensions slow down retrieval but often provide better accuracy.
EMBEDDING_DIM = 4096
assert EMBEDDING_DIM == 4096 or EMBEDDING_DIM <= 2048

# Load images into fast.ai's ImageDataBunch object
random.seed(642)
data_finetune = (
    ImageList.from_folder(DATA_FINETUNE_PATH)
    .split_by_rand_pct(valid_pct=0.05, seed=20)
    .label_from_folder()
    .transform(tfms=fastai.vision.transform.get_transforms(), size=IM_SIZE)
    .databunch(bs=BATCH_SIZE, num_workers=db_num_workers())
    .normalize(imagenet_stats)
)

print(
    f"Data for fine-tuning: {len(data_finetune.train_ds.x)} training images and {len(data_finetune.valid_ds.x)} validation images.")

learn = cnn_learner(
    data_finetune,
    ARCHITECTURE,
    metrics=[],
    ps=DROPOUT
)

print(learn.model[1])

# By default uses the 2048 dimensional pooling layer as implemented in the paper.
# Optionally can instead keep the 4096-dimensional pooling layer from the ResNet-50 model.
if EMBEDDING_DIM != 4096:
    modules = []
    pooling_dim = 2048
else:
    modules = [l for l in learn.model[1][:3]]
    pooling_dim = 4096

EmbeddedFeatureWrapper.__module__ = "model"
L2NormalizedLinearLayer.__module__ = "model"
# Add new layers
modules.append(EmbeddedFeatureWrapper(input_dim=pooling_dim,
                                      output_dim=EMBEDDING_DIM,
                                      dropout=DROPOUT))
modules.append(L2NormalizedLinearLayer(input_dim=EMBEDDING_DIM,
                                       output_dim=len(data_finetune.classes)))
learn.model[1] = nn.Sequential(*modules)

# Create new learner object since otherwise the new layers are not updated during backprop
learn = fastai.vision.Learner(data_finetune, learn.model)

# Update loss function
NormSoftmaxLoss.__module__ = "model"


learn.loss_func = FlattenedLoss(NormSoftmaxLoss)

# Edited model head
print(learn.model[1])

learn.fit_one_cycle(EPOCHS_HEAD, HEAD_LEARNING_RATE)
learn.unfreeze()
learn.fit_one_cycle(EPOCHS_BODY, BODY_LEARNING_RATE)

learn.export(file=Path(
    "/app/similarity_model.pkl"))
