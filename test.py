import multiprocessing
import numpy as np

arr = np.array([[[1, 2], [3, 4]],
                [[8, 2], [5, 4]]], dtype=np.uint8)

print(arr.shape)

# arr = np.array([1, 2, 3, 4], dtype=np.uint8)
# print(arr)
# print(arr.tobytes())
# print(np.frombuffer(arr.tobytes(), dtype=np.uint8).reshape((2, 2, 2)))

qty = int(646/8)
print(qty)

for i in range(1, 10):
    print(i)


# print(multiprocessing.cpu_count())
