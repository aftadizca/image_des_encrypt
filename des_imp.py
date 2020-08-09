# import numpy as np
# from bitarray import bitarray
import os
import io
import PIL.Image as Image
import numpy as np

from des import DesKey
# key = "12345678"

# pc1_table = np.array([[57, 49, 41, 33, 25, 17, 9],
#                       [1, 58, 50, 42, 34, 26, 18],
#                       [10, 2, 59, 51, 43, 35, 27],
#                       [19, 11, 3, 60, 52, 44, 36],
#                       [63, 55, 47, 39, 31, 23, 15],
#                       [7, 62, 54, 46, 38, 30, 22],
#                       [14, 6, 61, 53, 45, 37, 29],
#                       [21, 13, 5, 28, 20, 12, 4]])


# def permutation_one(key, table):
# key_bit = bitarray()
# key_bit.frombytes(key.encode('utf-8'))
# new_key = bitarray()

#     index = 1
#     for i in range(len(table)):
#         for j in range(len(table[i])):
#             if index == 29:
#                 new_key.extend('0000')
#                 new_key.append(key_bit[table[i][j]-1])
#                 index += 5
#             else:
#                 new_key.append(key_bit[table[i][j]-1])
#                 index += 1
#     new_key.extend('0000')
#     return new_key


# print(permutation_one(key, pc1_table))

# img = Image.open("convert.png")
# img_array = np.array(img)
# h, w, _ = img_array.shape
# print(h, w)

# for i in range(0, h, 2):
#     for j in range(w):
#         print(i)
#         # new_img_array[i, j] = np.append(img_array[i, j], [255])

arr = np.array([100, 100, 100, 100, 100, 100, 100, 100], dtype=np.uint8)
print(arr.dtype)
print(arr.tobytes())

key0 = DesKey(b"12345678")
a = key0.encrypt(arr.tobytes(), padding=False)
print(a)
print(np.frombuffer(a, dtype=np.uint8))

a = key0.decrypt(a, padding=False)
print(a)
print(np.frombuffer(a, dtype=np.uint8))

# image = Image.open(io.BytesIO(bytes(a)))
# image.save("hlo.png")
