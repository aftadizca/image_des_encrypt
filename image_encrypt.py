import numpy as np
from des2 import des, bin2hex
from hex2dec import hex2dec
from PIL import Image
import convert as cvt
import os
import multiprocessing
from multiprocessing import shared_memory
from time import perf_counter
import sys
from des import DesKey


def process_img(img_array, processed_px, i, k, mode):
    des = DesKey(bytes(key, encoding="utf-8"))
    if mode == 'e':
        enc_x = des.encrypt(img_array[i].tobytes(), padding=False)
    else:
        enc_x = des.decrypt(img_array[i].tobytes(), padding=False)
    enc_x = np.frombuffer(enc_x, dtype=np.uint8).reshape((480, 4))
    processed_px[i] = enc_x


def image_enc(mode, path, key):
    img_array = cvt.convert(path)
    print(img_array.shape)

    shm = shared_memory.SharedMemory(
        create=True, size=img_array.nbytes)

    processed_px = np.ndarray(
        img_array.shape, dtype=img_array.dtype, buffer=shm.buf)

    processes = []
    for i in range(0, img_array.shape[0]):
        process = multiprocessing.Process(target=process_img, args=(
            img_array, processed_px, i, key, mode,))
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
    start = perf_counter()
    key = "000000001111111122222222"
    image_enc('e', 'download.jpeg', key)
    end = perf_counter()
    print("elapsed : ", end - start, " second")
    # print(image_enc(sys.argv[1], sys.argv[2], sys.argv[3]))
    # print("Elapsed -", time.process_time() - t)
