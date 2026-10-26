import numpy as np, sys
from PIL import Image, ImageFilter
from scipy import ndimage
def cutout(im, thr=18, close=2):
    a = np.array(im.convert('RGB')).astype(int)
    white = (255 - a).max(-1) < thr
    lab, n = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    fg = ~bg
    fg = ndimage.binary_closing(fg, iterations=close)
    fg = ndimage.binary_fill_holes(fg)
    al = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert('RGBA'); out.putalpha(al)
    return out
