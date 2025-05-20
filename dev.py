import time
import serial
import socket
import numpy as np
import pyvisa as visa


def search():
  rm = visa.ResourceManager()
  devices = rm.list_resources()

  for device in devices: print(device)


def switch(channel):
  rm = visa.ResourceManager()
  device = rm.open_resource('GPIB0::17::INSTR')
  device.write(f'ROUT1:CHAN1 A,{channel}')
  device.close()


class Scpi:
  def __init__(self, host, port):
    self.socket = socket.socket()
    self.socket.connect((host, port))

  def write(self, command):
    self.socket.sendall(bytearray(f'{command}\n', 'utf-8'))

  def query(self, command):
    self.write(command)
    reply = ''
    while reply.find('\n') < 0:
      reply += self.socket.recv(1024).decode()
    return reply

  def close(self):
    self.socket.close()


class usbserial:
  def __init__(self, port):
    self.device = serial.Serial(port, 115200)

  def write(self, command):
    self.device.write(bytes(f'{command}\r', encoding='ascii'))
    time.sleep(0.2)

  def read(self, command):
    self.write(command)
    time.sleep(1)
    return self.device.read(self.device.in_waiting)

  def close(self):
    self.device.close()


class E_Tek_DLDC_1002:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::27::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    self.device.clear()
    text = self.device.query(command)
    text = text.encode('utf-8')
    text = str(text, 'utf-8')

    return text

  def close(self):
    self.device.close()


class Ando_AQ2105B_photodiode:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::19::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self):
    data = self.device.query('OD3')

    a = float(data[6:14])
    b = float(data[21:29])

    return a, b

  def setrg(self):
    self.write('RG')

  def close(self):
    self.device.close()


class Anritsu_MN9610A_attenuator:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::6::INSTR')

  def write(self, command):
    self.device.write(command)

  def value(self, level):
    self.write(f'ATT {level}')
    time.sleep(0.5)

  def close(self):
    self.device.close()


class Agilent_DSO1014A_oscilloscope:
  def __init__(self, command):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('USB0::0x0957::0x0588::CN50483638::INSTR')

    if command:
      self.write(command)
      self.close()

  def write(self, command):
    self.device.write(f':{command}')

  def query(self, command):
    return float(self.device.query(f':{command}'))

  def close(self):
    self.device.close()

  def getwave(self, ch):
    data = self.device.query(f':WAV:DATA? CHAN{ch}')
    data = data.replace(',', '')
    data = data.split(' ')[1:]
    data = np.array([v for v in data if v], np.float64)

    return data * 1000

  def setup(self):
    self.write('TIM:FORM YT')
    self.write('WAV:POINTS:MODE RAW')
    self.write('WAV:POINTS 10001')
    self.write('WAV:FORM ASCII')
    self.write('TIM:SCAL 0.001')
    self.write('TIM:FORM XY')
    self.write('RUN')
    time.sleep(1)


class ldc:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::4::INSTR')

  def write(self, command):
    self.device.write(f'{command};')

  def query(self, command):
    value = float(self.device.query(f'{command};'))
    time.sleep(0.5)
    return value

  def value(self, level):
    self.write(f'LAS:LDI {level}')
    self.on()
    time.sleep(0.5)

  def volt(self):
    return self.query('LAS:LDV?')

  def tec(self, temperature):
    self.write('TEC:MODE:T')
    self.write(f'TEC:T {temperature}')
    self.write('TEC:OUT ON')
    time.sleep(1)

  def on(self):
    self.write('LAS:OUT 1')

  def off(self):
    self.write('LAS:OUT 0')

  def close(self):
    self.device.close()


class Keysight_81630B_photodiode:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('TCPIP0::192.168.0.25::inst0::INSTR')
    self.device.timeout = 5000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def fetch(self, slot, ch):
    command = f'FETCH{slot}:CHAN{ch}:POW?'
    return float(self.device.query(command))

  def read(self, slot, ch):
    command = f'READ{slot}:CHAN{ch}:POW?'
    return float(self.device.query(command))

  def dBm(self, slot, ch):
    self.write(f'SENS{slot}:CHAN{ch}:POW:UNIT 0')

  def mW(self, slot, ch):
    self.write(f'SENS{slot}:CHAN{ch}:POW:UNIT 1')

  def close(self):
    self.device.close()


class Keysight_81630B_attenuator:
  def __init__(self, address):
    rm = visa.ResourceManager()
    self.device = rm.open_resource(address)
    self.device.timeout = 5000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class Viavi_Power_Meter_mOPM_C1:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('TCPIP0::192.168.0.107::inst0::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class Yokogawa_AQ6370D_GPIB:
  def __init__(self, command):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::5::INSTR')
    self.device.timeout = 50000

    if command:
      self.write(command)
      self.close()

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class Yokogawa_AQ6370D:
  def __init__(self, command):
    self.device = Scpi('192.168.0.30', 1024)
    self.device.query('open \"yokogawa\"')
    self.device.query('coherent')

    if command:
      self.write(command)
      self.close()

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class pdl:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::2::INSTR')
    self.device.write_termination = '\n'
    self.write('WAV 1550')

  def write(self, command):
    self.device.clear()
    self.device.write(command)

  def query(self):
    self.device.clear()
    data = self.device.query('READ?')
    return round(float(data[2:9]), 4), round(float(data[12:18]), 3)

  def close(self):
    self.device.close()


class Keysight_N7711A_tunalble_laser:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('TCPIP0::192.168.0.101::inst0::INSTR')
    self.device.timeout = 1000
    self.device.clear()

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    self.device.clear()
    return self.device.query(command)

  def close(self):
    self.device.close()


class Agilent_81640A_tunalble_laser:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::20::INSTR')

  def write(self, command):
    self.device.write(command)

  def wavelength(self, k):
    self.write(f'SOUR0:WAV {k}NM')
    time.sleep(1)

  def power(self, p):
    self.write(f'SOUR0:POW {p}DBM')

  def close(self):
    self.device.close()


class Santec_WSL_110_tunalble_laser:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::1::INSTR')
    self.device.timeout = 1000
    self.device.clear()

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    self.device.clear()
    return self.device.query(command)

  def close(self):
    self.device.close()


class Keysight_E3648A_power_supply:
  def __init__(self, address):
    rm = visa.ResourceManager()
    self.device = rm.open_resource(f'GPIB0::{address}::INSTR')
    self.device.timeout = 5000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class Agilent_E3831A_power_supply:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::6::INSTR')
    self.device.timeout = 5000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def close(self):
    self.device.close()


class ivs:
  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::10::INSTR')
    self.device.timeout = 50000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    data = self.device.query(command)
    data = data.split(',')
    return float(data[0]), float(data[1])

  def read2400(self):
    data = self.device.query(':READ?')
    data = data.split(',')
    
    volt, curr = [], []
    
    for i in range(len(data)):
      if i % 5 == 0: volt.append(float(data[i]))
      if i % 5 == 1: curr.append(float(data[i]))

    return volt, curr

  def Iread(self, n, ch):
    strs = f'printbuffer(1,{n},{ch}.nvbuffer1.readings)'
    data = self.device.query(strs)
    data = data.split(',')

    for i in range(len(data)): data[i] = float(data[i])

    return data

  def Vread(self, n, ch):
    strs = f'printbuffer(1,{n},{ch}.nvbuffer1.readings)'
    data = self.device.query(strs)
    data = data.split(',')

    for i in range(len(data)): data[i] = float(data[i])

    return data

  def close(self):
    self.device.close()


def Scpi_pd_test():
  pd = Scpi('192.168.0.25', 5025)
  print(pd.query('*IDN?'))
  try:
    while 1:
      print(float(pd.query('FETCH1:CHAN1:POW?')))
      time.sleep(0.5)
  except KeyboardInterrupt:
    pd.close()


if __name__ == '__main__':
  # search()
  Scpi_pd_test()
