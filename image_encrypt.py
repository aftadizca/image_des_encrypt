import numpy as np
import SharedArray as sa
from PIL import Image
import convert as cvt
import os
import multiprocessing
from time import perf_counter
import sys
from des import DesKey


def process_img(img_array, processed_px, i, qtyperprocess, k, mode, modulus=0):
    if modulus > 0:
        ranges = range(i*qtyperprocess, i*qtyperprocess+modulus)
    else:
        ranges = range(i*qtyperprocess, i*qtyperprocess+qtyperprocess)
    for j in ranges:
        des = DesKey(bytes(key, encoding="utf-8"))
        if mode == 'e':
            enc_x = des.encrypt(img_array[j].tobytes(), padding=False)
        else:
            enc_x = des.decrypt(img_array[j].tobytes(), padding=False)
        processed_px[j] = np.frombuffer(
            enc_x, dtype=np.uint8).reshape((480, 4))


def image_enc(mode, path, key):
    img_array = cvt.convert(path)
    # print("Image shape : ", img_array.shape)

    # # initialize shared memory
    # shm = shared_memory.SharedMemory(
    #     create=True, size=img_array.nbytes)
    # # create shared memory
    # processed_px = np.ndarray(
    #     img_array.shape, dtype=img_array.dtype, buffer=shm.buf)

    try:
        processed_px = sa.create("a", img_array.shape, dtype=img_array.dtype)
    except FileExistsError:
        sa.delete("a")
        processed_px = sa.create("a", img_array.shape, dtype=img_array.dtype)

    qtyperprocess = int(img_array.shape[0]/multiprocessing.cpu_count())
    modulus = img_array.shape[0] % multiprocessing.cpu_count()

    # create process
    processes = []
    for i in range(0, multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=process_img, args=(
            img_array, processed_px, i, qtyperprocess, key, mode,))
        processes.append(process)
        process.start()

    if modulus > 0:
        process = multiprocessing.Process(target=process_img, args=(
            img_array, processed_px, multiprocessing.cpu_count(), qtyperprocess, key, mode, modulus))
        processes.append(process)
        process.start()

    # wait process to completed
    for process in processes:
        process.join()

    # create new filename
    cpath, filename = os.path.split(path)
    filename = os.path.splitext(filename)[0].replace("_e", "")+"_"+mode+".png"
    cvt.save_image(processed_px, os.path.join(cpath, filename))

    # # close shared memory
    # shm.close()
    # shm.unlink()
    sa.delete("a")

    return os.path.join(cpath, filename)


if __name__ == "__main__":
    start = perf_counter()
    key = "000000001111111122222222"
    image_enc('d', 'test2_e.png', key)
    end = perf_counter()
    print(f"elapsed : {end - start:.3f} second")
    # print(image_enc(sys.argv[1], sys.argv[2], sys.argv[3]))
    # print("Elapsed -", time.process_time() - t)
