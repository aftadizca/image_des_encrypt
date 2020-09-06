import numpy as np
from PIL import Image
from time import perf_counter


def convert(path, maxWidth=0):
    img = Image.open(path)
    format = img.format
    # print("Image size : ", img.size)
    # print("Image format:", img.format)
    if maxWidth > 0:
        if maxWidth % 2 != 0:
            maxWidth = maxWidth + 1
        h = int(img.size[1]/img.size[0]*maxWidth)
        if h % 2 == 0:
            img = img.resize((maxWidth, h))
        else:
            img = img.resize((maxWidth, h+1))
    else:
        w = img.size[0]
        h = img.size[1]
        if img.size[0] % 2 != 0:
            w = w+1
        if img.size[1] % 2 != 0:
            h = h+1
        img = img.resize((w, h))

    if format == "PNG":
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
    t1 = perf_counter()
    save_image(convert("test.jpg"), "test.png")
    t2 = perf_counter()
    print(f"Time : {t2-t1:.2f} s")
