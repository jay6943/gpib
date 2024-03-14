import dev
import libximc.highlevel as ximc

port = [5, 12, 10, 14, 11, 9, 13, 15]
edge = [20000, 800, 800, 800, 800, 800, 800, 1300]
title = ['linear', 'Xin', 'Yin', 'Zin', 'Xout', 'Yout', 'Zout', 'vertical']
stop = 100

class Stage:
  def __init__(self, address):
    self.port = port[address]
    self.edge = edge[address]

    self.device = ximc.Axis(r'xi-com:\\.\COM' + str(port[address]))
    self.device.open_device()

  def close(self):
    self.device.close_device()

  def get_position(self):
    position = str(self.device.get_position()).split()

    return [position[1], position[3]]

  def get_speed(self):
    m = self.device.get_move_settings()
    return str(m.Speed)

  def set_speed(self, speed):
    if speed < 10: speed = 10
    if speed > 2000: speed = 2000

    m = self.device.get_move_settings()
    m.Speed = speed
    self.device.set_move_settings(m)

  def set_zero(self):
    self.device.command_zero()

  def get_edges(self):
    edges = str(self.device.get_edges_settings()).split()
    return [edges[5], edges[9]]

  def go_home(self):
    self.set_speed(1000)
    self.device.command_home()
    self.device.command_wait_for_stop(stop)

  def move_to(self, there, microsteps):
    self.set_speed(abs(there - int(self.get_position()[0])) * 2)
    self.device.command_move(there, microsteps)
    self.device.command_wait_for_stop(stop)

  def shift_on(self, steps, microsteps):
    self.set_speed(abs(steps) * 2)
    self.device.command_movr(steps, microsteps)
    self.device.command_wait_for_stop(stop)

  def find_max(self, steps, microsteps):
    n, y, a, b = 20, [], [], []
    x = [i for i in range(2 * n + 1)]
    macro = -steps * n
    micro = divmod(microsteps * n, 256)

    self.shift_on(macro - micro[0], -micro[1])

    pd = dev.Keysight_81630B_photodiode()
    for i in x:
      position = self.get_position()
      power = pd.read(1, 1)
      y.append(power)
      a.append(position[0])
      b.append(position[1])
      print(i, position, power)
      self.shift_on(steps, microsteps)
    imax = y.index(max(y))
    self.move_to(int(a[imax]), int(b[imax]))
    ymax = pd.read(1, 1)
    pd.close()

    return a[imax], b[imax], ymax


if __name__ == '__main__':
  axis = Stage(0)
  print(axis.get_position())
