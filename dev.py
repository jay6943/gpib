import time
import serial
import numpy as np
import pyvisa as visa

def search():
  rm = visa.ResourceManager()
  devices = rm.list_resources()

  for idn in devices:
    print(idn)
    if idn[0] == 'G':
      device = rm.open_resource(idn)
      print(device.query('*IDN?'))
      device.close()

def switch(channel):
  rm = visa.ResourceManager()
  device = rm.open_resource('GPIB0::17::INSTR')
  device.write('ROUT1:CHAN1 A,' + str(channel))
  device.close()

class Ando_AQ2105B_photodiode:

  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::19::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self):
    data = self.device.query('OD3')

    a = float(data[ 6:14])
    b = float(data[21:29])

    return a, b

  def setrg(self):
    self.write('RG')

  def close(self):
    self.device.close()

class att:

  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::6::INSTR')

  def write(self, command):
    self.device.write(command)

  def value(self, level):
    self.write('ATT ' + str(level))
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
    self.device.write(':' + command)

  def query(self, command):
    return float(self.device.query(':' + command))

  def close(self):
    self.device.close()

  def getwave(self, ch):
    data = self.device.query(':WAV:DATA? CHAN' + str(ch))
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
    self.device.write(command + ';')

  def query(self, command):
    value = float(self.device.query(command + ';'))
    time.sleep(0.5)
    return value

  def value(self, level):
    self.write('LAS:LDI ' + str(level))
    self.on()
    time.sleep(0.5)

  def volt(self):
    return self.query('LAS:LDV?')

  def tec(self, temperature):
    self.write('TEC:MODE:T')
    self.write('TEC:T ' + str(temperature))
    self.write('TEC:OUT ON')
    time.sleep(1)

  def on(self):
    self.write('LAS:OUT 1')

  def off(self):
    self.write('LAS:OUT 0')

  def close(self):
    self.device.close()

class opm:

  def __init__(self, gpib):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::' + str(gpib) + '::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self, slot, ch):
    command = 'FETCH' + str(slot) + ':CHAN' + str(ch) + ':POW?'
    return float(self.device.query(command))

  def read(self, slot, ch):
    command = 'READ' + str(slot) + ':CHAN' + str(ch) + ':POW?'
    return float(self.device.query(command))

  def dBm(self, slot, ch):
    self.write('SENS' + str(slot) + ':CHAN' + str(ch) + ':POW:UNIT 0')

  def mW(self, slot, ch):
    self.write('SENS' + str(slot) + ':CHAN' + str(ch) + ':POW:UNIT 1')
      
  def close(self):
    self.device.close()

class osa:

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
    self.device = rm.open_resource('GPIB0::20::INSTR')

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    self.device.clear()
    return self.device.query(command)

  def wavelength(self, k):
    self.write('SOUR1:WAV ' + str(k) + 'NM')
    time.sleep(1)

  def power(self, p):
    self.write('SOUR1:POW ' + str(p) + 'DBM')

  def close(self):
    self.device.close()

class Agilent_81640A_tunalble_laser:

  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::20::INSTR')

  def write(self, command):
    self.device.write(command)

  def wavelength(self, k):
    self.write('SOUR0:WAV ' + str(k) + 'NM')
    time.sleep(1)

  def power(self, p):
    self.write('SOUR0:POW ' + str(p) + 'DBM')

  def close(self):
    self.device.close()

class Santec_WSL_tunalble_laser:

  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::1::INSTR')

  def write(self, command):
    self.device.write(command)

  def wavelength(self, k):
    self.write('SOUR0:WAV ' + str(k) + 'NM')
    time.sleep(1)

  def power(self, p):
    self.write('SOUR0:POW ' + str(p) + 'DBM')

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
    
    V, I = [], []
    
    for i in range(len(data)):
      if i % 5 == 0: V.append(float(data[i]))
      if i % 5 == 1: I.append(float(data[i]))

    return V, I

  def Iread(self, n, ch):
    strs = 'printbuffer(1,' + str(n) + ',' + ch + '.nvbuffer1.readings)'
    data = self.device.query(strs)
    data = data.split(',')

    for i in range(len(data)): data[i] = float(data[i])

    return data

  def Vread(self, n, ch):
    strs = 'printbuffer(1,' + str(n) + ',' + ch + '.nvbuffer1.readings)'
    data = self.device.query(strs)
    data = data.split(',')

    for i in range(len(data)): data[i] = float(data[i])

    return data

  def close(self):
    self.device.close()

class dcp:

  def __init__(self):
    rm = visa.ResourceManager()
    self.device = rm.open_resource('GPIB0::6::INSTR')
    self.device.timeout = 50000

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    data = self.device.query(command)
    data = data.split(',')
    return float(data[0]), float(data[1])

  def close(self):
    self.device.close()

class usbserial:

  def __init__(self, port):
    self.device = serial.Serial(port, 115200)
  
  def write(self, command):
    self.device.write(bytes(command + '\r', encoding='ascii'))
    time.sleep(0.2)

  def read(self, command):
    self.write(command)
    time.sleep(1)
    return self.device.read(self.device.in_waiting)

  def close(self):
    self.device.close()

if __name__ == '__main__':
  search()

  '''
  iq = dso(False)
  iq.write('TIM:FORM YT')
  iq.write('TIM:SCAL ' + str(float(1000 * 1e-6)))
  iq.write('WAV:POINTS:MODE RAW')
  iq.write('WAV:POINTS ' + str(100))
  iq.write('WAV:FORM ASCII')
  iq.write('SINGLE')

  time.sleep(2)

  data = iq.getwave(1)
  '''