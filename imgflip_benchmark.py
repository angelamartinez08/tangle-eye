#!/usr/bin/env python3
"""
benchmark drawing images in psyhcopy
"""

from psychopy import visual
import timeit
import tempfile
import logging
from PIL import Image
from typing import Tuple
import os
import numpy as np

N_imgs = 10
N_iter = 100

logging.basicConfig(level=logging.INFO)

def random_image(fname=None, img_size=(256,256)):
    """
    generate an image of specified size
    :param fname: save location. if not provied will be temp file with .png extention
    """
    if fname is None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            fname = tmp.name + '.png'
            logging.info("saving to %s", fname)
    arr = np.random.randint(0, 256, (*img_size, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    img.save(fname)
    return(fname)

win = visual.Window([1024,786])
imgs_small = [random_image() for _ in range(N_imgs)]
img_large = random_image(img_size=win.size)

tex_many = [visual.ImageStim(win, fname, name=fname) for fname in imgs_small]
tex_larg = visual.ImageStim(win, img_large)

def rand_pos() -> Tuple[float, float]:
    """random position for placing image
    TODO: consider image size to make sure it's entirely on scren?
    """
    return (np.random.rand()*4-2, np.random.rand()*4-2)

def draw_many():
    """many small images"""
    win.flip()
    for i in range(len(tex_many)):
        tex_many[i].pos = rand_pos()
        tex_many[i].draw()
    win.flip()

def draw_one():
    """one large image"""
    win.flip()
    tex_larg.pos = rand_pos()
    tex_larg.draw()
    win.flip()


t_many = timeit.timeit(draw_many, number=N_iter)
t_one  = timeit.timeit(draw_one, number=N_iter)

print(f"flipped {N_imgs} images in {t_many/N_iter:.03f}s per iteration")
print(f"one large image flipped {t_one/N_iter:.03f}s per iteration")

# remove tmp images
for f in imgs_small + [img_large]:
    logging.debug('remove %s', f)
    os.unlink(f)
