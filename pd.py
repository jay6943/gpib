import dev
import keyboard
import matplotlib.pyplot as plt

x = []
y = []

pd = dev.Keysight_81630B_photodiode()

plt.ion()
fig, ax = plt.subplots(figsize=(12, 8))

while True:
  if keyboard.is_pressed('esc'):
    break

  y.append(pd.fetch(1, 1))

  ax.clear()
  ax.plot(y)
  ax.grid()

  plt.show()
  plt.pause(0.3)

plt.close()
pd.close()
