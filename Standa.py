import libximc.highlevel as ximc

def get_position(stage):
  stage.open_device()
  position = str(stage.get_position()).split()
  stage.close_device()

  return position[1]


class linear:
  def __init__(self):
    self.axis = ximc.Axis(r'xi-com:\\.\COM13')

  def get_position(self):
    return get_position(self.axis)

  def set_speed(self, speed):
    self.axis.open_device()
    m = self.axis.get_move_settings()
    m.Speed = speed
    self.axis.set_move_settings(m)
    self.axis.close_device()

  def move(self, steps, microsteps):
    self.axis.open_device()
    self.axis.command_movr(steps, microsteps)
    self.axis.command_wait_for_stop(500)
    self.axis.close_device()

  def move_speed(self, steps, microsteps, speed):
    self.axis.open_device()
    m = self.axis.get_move_settings()
    m.Speed = speed
    self.axis.set_move_settings(m)
    self.axis.command_movr(steps, microsteps)
    self.axis.command_wait_for_stop(500)
    self.axis.close_device()


class vertical:
  def __init__(self):
    self.axis = ximc.Axis(r'xi-com:\\.\COM14')

  def get_position(self):
    return get_position(self.axis)

  def go_home(self):
    self.axis.open_device()
    self.axis.command_home()
    self.axis.command_wait_for_stop(500)
    self.axis.command_stop()
    self.axis.close_device()

  def move(self, steps, microsteps):
    self.axis.open_device()
    self.axis.command_movr(steps, microsteps)
    self.axis.command_wait_for_stop(500)
    self.axis.close_device()

  def move_speed(self, steps, microsteps, speed):
    self.axis.open_device()
    m = self.axis.get_move_settings()
    m.Speed = speed
    self.axis.set_move_settings(m)
    self.axis.command_movr(steps, microsteps)
    self.axis.command_wait_for_stop(500)
    self.axis.close_device()
