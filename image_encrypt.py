import numpy as np
from des2 import des, bin2hex
from hex2dec import hex2dec
from PIL import Image
import convert as cvt
import os
import multiprocessing
from multiprocessing import shared_memory
import time
import sys

t = time.process_time()


def process_img(img_array, processed_px, i, k, mode):
    for j in range(img_array.shape[1]):
        px = np.append(img_array[i, j], img_array[i+1, j]
                       ).tobytes().hex().upper()
        enc_x = hex2dec(bin2hex(des(px, k, mode)))
        processed_px[i, j] = enc_x[0]
        processed_px[i+1, j] = enc_x[1]


def image_enc(mode, path, key):
    k = bytes(key, encoding='utf-8').hex().upper()
    img_array = cvt.convert(path)

    shm = shared_memory.SharedMemory(
        create=True, size=img_array.nbytes)

    processed_px = np.ndarray(
        img_array.shape, dtype=img_array.dtype, buffer=shm.buf)

    processes = []
    for i in range(0, img_array.shape[0], 2):
        process = multiprocessing.Process(target=process_img, args=(
            img_array, processed_px, i, k, mode,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    cpath, filename = os.path.split(path)

    filename = os.path.splitext(filename)[0].replace("_e", "")+"_"+mode+".png"
    cvt.save_image(processed_px, os.path.join(cpath, filename))
    shm.close()
    shm.unlink()
    return os.path.join(cpath, filename)


if __name__ == "__main__":
    key = "12345678"
    image_enc('e', 'test2.jpg', key)
    # print(image_enc(sys.argv[1], sys.argv[2], sys.argv[3]))
    # print("Elapsed -", time.process_time() - t)
