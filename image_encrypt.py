import numpy as np
from des2 import des, bin2hex
from hex2dec import hex2dec
from PIL import Image
import convert as cvt
import os
import time


def image_enc(path, mode, key):
    k = bytes(key, encoding='utf-8').hex().upper()
    img_array = cvt.convert(path)

    for i in range(0, cvt.h, 2):
        for j in range(cvt.w):
            px = np.append(img_array[i, j], img_array[i+1, j]
                           ).tobytes().hex().upper()
            enc_x = hex2dec(bin2hex(des(px, k, mode)))
            img_array[i, j] = enc_x[0]
            img_array[i+1, j] = enc_x[1]

    filename = os.path.splitext(os.path.basename(path))[
        0].replace("_e", "")+"_"+mode+".png"
    cvt.save_image(img_array, filename)


t = time.process_time()
key = "12345678"
image_enc("test2.jpg", 'e', key)
print("Elapsed -", time.process_time() - t)
