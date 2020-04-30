import os
import re
from multiprocessing import Process
from subprocess import call
import Augmentor

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("augment_amount", type=int, default=24,
                    help="augmented images per class")
parser.add_argument('--path',
                    help='Path to duplicate')

args = parser.parse_args()
# load image


def f():
    for folder in os.listdir(args.path):
        p = Augmentor.Pipeline(args.path+folder)
        p.random_distortion(probability=1, grid_width=4,
                            grid_height=4, magnitude=8)
        p.zoom_random(0.9, percentage_area=0.85)
        p.sample(args.augment_amount)


if __name__ == '__main__':
    p = Process(target=f)
    p.start()
    p.join()
