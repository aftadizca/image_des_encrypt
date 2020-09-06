import numpy as np
import time
from multiprocessing import Pool, RawArray
import convert as cvt
import os
from des import DesKey
from time import perf_counter
from PIL import Image

# A global dictionary storing the variables passed from the initializer.
var_dict = {}


def init_worker(X, X_shape, key, mode):
    # Using a dictionary is not strictly necessary. You can also
    # use global variables.
    var_dict['X'] = X
    var_dict['X_shape'] = X_shape
    var_dict['key'] = key
    var_dict['mode'] = mode


def worker_func(i):
    # Simply computes the sum of the i-th row of the input matrix X
    # X_np = np.frombuffer(var_dict['X'], dtype=np.uint8).reshape(
    #     var_dict['X_shape'])
    # time.sleep(1)  # Some heavy computations
    # return np.asscalar(np.sum(X_np[i, :]))

    des = DesKey(bytes(var_dict['key'], encoding="utf-8"))
    img_array = np.frombuffer(
        var_dict['X'], dtype=np.uint8).reshape(var_dict['X_shape'])

    if var_dict['mode'] == 'e':
        enc_x = des.encrypt(img_array[i].tobytes(), padding=False)
    else:
        enc_x = des.decrypt(img_array[i].tobytes(), padding=False)
    enc_x = np.frombuffer(enc_x, dtype=np.uint8).reshape(
        (var_dict['X_shape'][1], var_dict['X_shape'][2]))
    return enc_x


def image_enc(mode, image_path, key):
    data = cvt.convert(image_path, maxWidth=480)
    print(data.shape)
    X_shape = data.shape
    X = RawArray('B', X_shape[0] * X_shape[1] * X_shape[2])
    # Wrap X as an numpy array so we can easily manipulates its data.
    X_np = np.frombuffer(X, dtype=np.uint8).reshape(X_shape)
    # Copy data to our shared array.
    np.copyto(X_np, data)
    # Start the process pool and do the computation.
    # Here we pass X and X_shape to the initializer of each worker.
    # (Because X_shape is not a shared variable, it will be copied to each
    # child process.)
    with Pool(initializer=init_worker, initargs=(X, X_shape, key, mode)) as pool:
        result = pool.map(worker_func, range(X_shape[0]))

    cpath, filename = os.path.split(image_path)
    file_split = os.path.splitext(filename)
    filename = file_split[0].replace("_e", "")+"_"+mode+".png"
    # im = Image.fromarray(np.array(result))
    # print(im.mode)
    # im = im.convert("RGB")
    # print(im.mode)
    # im.save(os.path.join(cpath, filename), quality=90)
    cvt.save_image(np.array(result), os.path.join(cpath, filename))
    return os.path.join(cpath, filename)


# We need this check for Windows to prevent infinitely spawning new child
# processes.
if __name__ == '__main__':
    start = perf_counter()
    print(image_enc('d', 'test.jpg', '12345678'))
    end = perf_counter()
    print("elapsed : ", end - start, " second")
