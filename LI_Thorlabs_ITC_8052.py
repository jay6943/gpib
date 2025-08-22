import time
import pyvisa as visa


class Thorlabs_ITC_8052:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::10::INSTR')
    self.device.timeout = 5000

  def write(self, command):
    self.device.write(command)
    time.sleep(0.5)

  def query(self, command):
    data = self.device.query(command)
    return data.split(' ')[-1]

  def read(self, command):
    return float(self.query(command))

  def close(self):
    self.device.control_ren(6)
    self.device.close()

  def set_current(self, current):
    self.write(f':ild:set {current * 0.001:.4f}')
    return self.read(':vld:act?')

  def set_temperature(self, temperature):
    self.write(f':temp:set {temperature:.1f}')


def reset():
  ld = Thorlabs_ITC_8052()
  ld.write('*RST')
  ld.close()


def laser_on(current):
  ld = Thorlabs_ITC_8052()
  ld.set_current(current)
  ld.write(':laser on')
  ld.close()


def laser_off():
  ld = Thorlabs_ITC_8052()
  ld.write(':laser off')
  ld.close()


def tec_on(temperature):
  ld = Thorlabs_ITC_8052()
  ld.set_temperature(temperature)
  ld.write(':tec on')
  ld.close()


def tec_off():
  ld = Thorlabs_ITC_8052()
  ld.write(':tec off')
  ld.close()
