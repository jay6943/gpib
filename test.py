import numpy as np


def varray():
  a = [i * 0.1 + 0.5 for i in range(7)]
  b = [(i + 1) * 0.02 + 1.1 for i in range(20)]
  d = np.round(np.array(a + b), 3)

  print(d)


if __name__ == '__main__': varray()
