from utils_cv.common.gpu import db_num_workers, which_processor
from utils_cv.common.data import unzip_url
from utils_cv.classification.data import Urls
from utils_cv.classification.widget import ResultsWidget
from utils_cv.classification.plot import plot_pr_roc_curves
from utils_cv.classification.model import TrainMetricsRecorder
from fastai.vision import (
    models, ImageList, imagenet_stats, partial, cnn_learner, ClassificationInterpretation, to_np,
)
from fastai.metrics import accuracy
import fastai

from pathlib import Path
import numpy as np
import sys


# fastai and torch

# local modules

print(f"Fast.ai version = {fastai.__version__}")
which_processor()

#DATA_PATH = unzip_url(Urls.fridge_objects_path, exist_ok=True)
EPOCHS = 10
LEARNING_RATE = 1e-4
IM_SIZE = 300

BATCH_SIZE = 16
ARCHITECTURE = models.resnet18
path = Path('/app/classifier_data/')

data = (
    ImageList.from_folder(path)
    .split_by_rand_pct(valid_pct=0.2, seed=10)
    .label_from_folder()
    .transform(size=IM_SIZE)
    .databunch(bs=BATCH_SIZE, num_workers=db_num_workers())
    .normalize(imagenet_stats)
)

print(f'number of classes: {data.c}')
print(data.classes)

learn = cnn_learner(
    data,
    ARCHITECTURE,
    metrics=[accuracy],
    callback_fns=[partial(TrainMetricsRecorder, show_graph=True)]
)
learn.unfreeze()
learn.fit(EPOCHS, LEARNING_RATE)
learn.export(file=Path(
    "/app/classifier_model.pkl"))
_, validation_accuracy = learn.validate(
    learn.data.valid_dl, metrics=[accuracy])
print(f'Accuracy on validation set: {100*float(validation_accuracy):3.2f}')
