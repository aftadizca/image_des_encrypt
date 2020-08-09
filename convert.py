import numpy as np
from PIL import Image


def convert(path):
    img = Image.open(path)
    if img.size[0] != 480:
        h = int(img.size[1]/img.size[0]*480)
        if h % 2 == 0:
            img = img.resize((480, h))
        else:
            img = img.resize((480, h+1))
    if img.format == "PNG":
        # print("Format PNG")
        return np.array(img, dtype=np.uint8)
    else:
        # print("Format", img.format)
        img_array = np.array(img, dtype=np.uint8)
        img_array = np.insert(img_array, 3, 255, axis=2)
        return img_array


def save_image(img_array, name):
    new_img = Image.fromarray(img_array)
    new_img.save(name)


def getpixelvalue(path, x, y):
    img = Image.open("convert.png")
    img_array = np.array(img)
    return img_array[0, 0]


if __name__ == "__main__":
    save_image(convert("test2.jpg"), "convert.png")
