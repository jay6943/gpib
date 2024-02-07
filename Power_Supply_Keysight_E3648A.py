import dev
import time
import keyboard
import numpy as np


def keyboard_escape(running):
  print('\b' * 200, end='')
  for i in range(80):
    if keyboard.is_pressed('down arrow'):
      running = 0
      break

    print('-', end=' ')
    time.sleep(0.2)
  print('\b' * 200, end='')

  return running


def updown():
  ps = dev.Keysight_E3648A_power_supply(12)
  print(ps.query('*IDN?'))
  ps.write('INST:SEL OUT2')
  ps.write('VOLT:RANG HIGH')

  v = np.round(np.linspace(0, 15, 16), 1)

  running = 1

  while running:
    for volt in v:
      print('\b' * 20, end='')
      print('Voltage = ' + str(volt), end='')
      ps.write('VOLT ' + str(volt))
      time.sleep(0.1)
    for volt in v[::-1]:
      print('\b' * 20, end='')
      print('Voltage = ' + str(volt), end='')
      ps.write('VOLT ' + str(volt))
      time.sleep(0.1)

    running = 1 if keyboard_escape(running) else 0

  ps.close()

if __name__ == '__main__': updown()
