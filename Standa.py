import libximc.highlevel as ximc


port = [5, 12, 10, 14, 11, 9, 13, 15]
edge = [20000, 800, 800, 800, 800, 800, 800, 1300]


def device(address):
  return ximc.Axis(r'xi-com:\\.\COM' + str(address))


def get_position(axis):
  axis.open_device()
  position = str(axis.get_position()).split()
  axis.close_device()

  return position[1]


def get_speed(axis):
  axis.open_device()
  m = axis.get_move_settings()
  axis.close_device()

  return str(m.Speed)


def set_speed(axis, speed):
  axis.open_device()
  m = axis.get_move_settings()
  m.Speed = speed
  axis.set_move_settings(m)
  axis.close_device()


def set_zero(axis):
  axis.open_device()
  axis.command_zero()
  axis.close_device()


def get_edges(axis):
  axis.open_device()
  edges = str(axis.get_edges_settings()).split()
  axis.close_device()

  return [edges[5], edges[9]]


def go_home(axis):
  axis.open_device()
  axis.command_home()
  axis.command_wait_for_stop(500)
  axis.close_device()


def move_to(axis, position, microsteps):
  axis.open_device()
  axis.command_move(position, microsteps)
  axis.command_wait_for_stop(500)
  axis.close_device()


def shift_on(axis, steps, microsteps):
  axis.open_device()
  axis.command_movr(steps, microsteps)
  axis.command_wait_for_stop(500)
  axis.close_device()


if __name__ == '__main__':
  linear_step = 4162
  # linear_axis = device(5)
  # set_speed(linear_axis, 2000)
  # shift_on(linear_axis, linear_step, 0)
  # shift_on(linear_axis, -linear_step, 0)
