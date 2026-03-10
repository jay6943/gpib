import socket


class Scpi:
  def __init__(self, host, port):
    self.socket = socket.socket()
    self.socket.connect((host, port))

  def write(self, command):
    self.socket.sendall(bytearray(f'{command}\n', 'utf-8'))

  def query(self, command):
    self.write(command)
    return self.socket.recv(1024).decode().strip()

  def read(self, command):
    self.write(command)
    return self.socket.recv(32768).decode().strip()

  def close(self):
    self.socket.close()


class AQ6370D:
  def __init__(self, command):
    self.device = Scpi('192.168.0.30', 1024)
    self.query('open \"yokogawa\"')
    self.query('coherent')

    if command:
      self.write(command)
      self.close()

  def write(self, command):
    self.device.write(command)

  def query(self, command):
    return self.device.query(command)

  def read(self, command):
    return self.device.read(command)

  def close(self):
    self.device.close()


def OnMax():
  AQ6370D(':CALC:MARK:MAX')


def OnMin():
  AQ6370D(':CALC:MARK:MIN')


def OnMarkCenter():
  AQ6370D(':CALC:MARK:SCEN')


def OnContinuous():
  osa = AQ6370D(False)
  osa.write(':INIT:SMOD REP')
  osa.write(':INIT:IMM')
  osa.close()


def OnSingle():
  osa = AQ6370D(False)
  osa.write(':INIT:SMOD SING')
  osa.write(':INIT:IMM')
  osa.close()
