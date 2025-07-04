import pyvisa as visa


def test():
  ni = visa.ResourceManager()
  device = ni.open_resource('TCPIP0::192.168.0.19::inst0::INSTR')
  print(device.query('*IDN?'))
  device.close()

if __name__ == '__main__':
  test()
