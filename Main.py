#! /usr/bin/env python3
import os
import sys
from xml.dom import minidom

import matplotlib.pyplot as plt
import numpy as np
from pyfld import FastLineDetector
from PIL import Image, ImageFilter, ImageDraw
import click

BORDER_SIZE = 3
IMAGE_SIZE = (100, 100)
MIN_V = 0.01 * 255
THRESHOLD1 = 150
THRESHOLD2 = 250
THRESHOLD3 = 90
APERTURE_SIZE = 3
WIDTH = 100
HEIGHT = 100

def clean_img(img: Image.Image, image_size: tuple[int, int] = (100, 100)):
    return img.convert("L").resize(image_size)

def build_xml(x1: np.ndarray, x2: np.ndarray, y1: np.ndarray, y2: np.ndarray):
    root = minidom.Document()

    xml = root.createElement("BOARD")
    root.appendChild(xml)

    dims = root.createElement("DIMENSIONS")
    dims.setAttribute("width", str(WIDTH))
    dims.setAttribute("height", str(HEIGHT))
    xml.appendChild(dims)

    for i in range(len(x1)):
        wall = root.createElement("WALL")
        wall.setAttribute("x_1", f"{x1[i]:.2f}")
        wall.setAttribute("x_2", f"{x2[i]:.2f}")
        wall.setAttribute("y_1", f"{y1[i]:.2f}")
        wall.setAttribute("y_2", f"{y2[i]:.2f}")
        xml.appendChild(wall)

    return root

def draw_over_img(img: Image.Image, x1: np.ndarray, x2: np.ndarray, y1: np.ndarray, y2: np.ndarray, line_width: int = 1):
    draw = ImageDraw.Draw(img)
    for i in range(len(x1)):
        draw.line((x1[i], y1[i], x2[i], y2[i]), fill=(255, 0, 0), width=line_width)

@click.command("make-map")
@click.argument("FILE_PATH", type=click.Path(exists=True, dir_okay=False))
@click.option("--make-img", type=bool, help="if True, outputs the created lines to an image file", is_flag=True)
@click.option("--length-threshold", type=int, help="segments shorter than this will be discarded", default=5)
@click.option("--distance-threshold", type=float, help="a point placed from a hypothesis line segment farther than this will be regarded as an outlier", default=np.sqrt(2))
@click.option("--canny-th1", type=float, help="lower threshold in canny alg: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html", default=40)
@click.option("--canny-th2", type=float, help="upper threshold in canny alg: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html", default=150)
@click.option("--aperture-size", type=int, help="size of kernel in canny alg", default=3)
def make_map(file_path: str, make_img: bool, length_threshold: int, distance_threshold: float, canny_th1: float, canny_th2: float, aperture_size: int):
    print(file_path, length_threshold)
    fname = file_path.split(".")[-2].split(os.sep)[-1]
    xml_fname = fname + ".xml"

    img = Image.open(file_path)
    img = clean_img(img)
    arr = np.array(img)

    fld = FastLineDetector(length_threshold, distance_threshold, canny_th1, canny_th2, aperture_size, False)
    (x1, y1, x2, y2), _ = fld.detect(arr)

    root = build_xml(x1, x2, y1, y2)
    with open(xml_fname, 'w') as fp:
        fp.write(root.toprettyxml(indent="    "))

    if make_img:
        img_fname = fname + "_lines.jpg"

        out_img = Image.fromarray(np.zeros(arr.shape)).convert("RGB")
        
        draw_over_img(out_img, x1, x2, y1, y2)

        out_img.save(img_fname)


if __name__ == "__main__":
    make_map()
    exit(0)

    fig, ax = plt.subplots()
    ax.imshow(arr, cmap="gray")
    ax.plot([x1, x2], [y1, y2], c="r")
    fig.savefig(out_fname)

    fig, ax = plt.subplots()
    ax.imshow(np.zeros(arr.shape), cmap="gray")
    ax.plot([x1, x2], [y1, y2], c="r")
    fig.savefig("blank_" + out_fname)
