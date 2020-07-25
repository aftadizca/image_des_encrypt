#scramble.py
from PIL import Image
import sys
import os
import random
import argparse

def openImage(path):
    return Image.open(path)

def seed(key):
    random.seed(key)
 
def getFileName(path):
    return os.path.basename(path)

def getPixels(img):
    w, h = img.size
    pxs = []
    for x in range(w):
        for y in range(h):
            pxs.append(img.getpixel((x, y)))
    return pxs

def scrambledIndex(pxs):
    idx = list(range(len(pxs)))
    random.shuffle(idx)
    return idx

def scramblePixels(img, key):
    seed(key)
    pxs = getPixels(img)
    idx = scrambledIndex(pxs)
    out = []
    for i in idx:
        out.append(pxs[i])
    return out

def unScramblePixels(img, key):
    seed(key)
    pxs = getPixels(img)
    idx = scrambledIndex(pxs)
    out = list(range(len(pxs)))
    cur = 0
    for i in idx:
        out[i] = pxs[cur]
        cur += 1
    return out

def storePixels(name, size, pxs):
    outImg = Image.new("RGB", size)
    w, h = size
    pxIter = iter(pxs)
    for x in range(w):
        for y in range(h):
            outImg.putpixel((x, y), pxIter.__next__())
    outImg.save(name)

def main(path, action, key):
    img = openImage(path)
    if action == "s":
        pxs = scramblePixels(img, key)
        storePixels(getFileName(path), img.size, pxs)
    elif action == "us":
        pxs = unScramblePixels(img, key)
        storePixels(getFileName(path), img.size, pxs)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scramble image")
    ap.add_argument("-p","--img-path", required=True, type=str)
    ap.add_argument("-a","--action", required=True, type=str, choices=["s","us"], help="s=scramble & us=unscramble")
    ap.add_argument("-k","--key", required=True, type=str, help="key")
    args = vars(ap.parse_args())
    main(args['img_path'],args['action'],args['key'])
