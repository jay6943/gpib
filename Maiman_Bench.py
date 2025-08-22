import time
import serial


class Maiman_Laser_TEC:
  def __init__(self):
    self.device = serial.Serial('COM4', 115200)

  def write(self, command):
    self.device.write(bytearray(f'{command}\r', 'utf-8'))
    time.sleep(0.5)

  def query(self, command):
    self.write(command)
    data = self.device.read(self.device.in_waiting)
    return data.decode().split(' ')[-1]

  def read(self, command):
    return float(self.query(command))

  def close(self):
    self.device.close()

  def set_current(self, current):
    self.write(f'curr:value {current:.4f}')
    return self.read('volt:real?')

  def set_temperature(self, temperature):
    self.write(f'tec:temp:value {temperature:.1f}')


def reset():
  ld = Maiman_Laser_TEC()
  ld.write('*RST')
  ld.close()


def laser_on(current):
  ld = Maiman_Laser_TEC()
  ld.set_current(current)
  ld.write('dev:start on')
  ld.close()


def laser_off():
  ld = Maiman_Laser_TEC()
  ld.write('dev:start off')
  ld.close()


def tec_on(temperature):
  ld = Maiman_Laser_TEC()
  ld.set_temperature(temperature)
  ld.write('tec:start on')
  ld.close()


def tec_off():
  ld = Maiman_Laser_TEC()
  ld.write('tec:start off')
  ld.close()
