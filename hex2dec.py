
import numpy as np


def hex2dec(text):
    mp = {'0': "0",
          '1': "1",
          '2': "2",
          '3': "3",
          '4': "4",
          '5': "5",
          '6': "6",
          '7': "7",
          '8': "8",
          '9': "9",
          'A': "10",
          'B': "11",
          'C': "12",
          'D': "13",
          'E': "14",
          'F': "15"}

    a = []
    for i in range(0, len(text), 2):
        a.append(int(mp[text[i]])*16 + int(mp[text[i+1]]))

    a = np.array(a, dtype=np.uint8).reshape(2, 4)
    return a

    a = []
    for i in range(0, len(text), 2):
        a.append(int(mp[text[i]])*16 + int(mp[text[i+1]]))

    a = np.array(a, dtype=np.uint8).reshape(2, 4)
    return a


if __name__ == "__main__":
    s = 'C4DE7B0479FCFDAA'
    print(hex2dec(s).tobytes().hex())
    # print(bytes('12345678', encoding='utf-8').hex().upper())
