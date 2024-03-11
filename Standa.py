import libximc.highlevel as ximc

port = [5, 12, 10, 14, 11, 9, 13, 15]
edge = [20000, 800, 800, 800, 800, 800, 800, 1300]
stop = 100


def get_device(address):
  axis = ximc.Axis(r'xi-com:\\.\COM' + str(port[address]))
  axis.open_device()

  return axis


def get_position(address):
  axis = get_device(address)
  position = str(axis.get_position()).split()
  axis.close_device()

  return position[1]


def get_uposition(address):
  axis = get_device(address)
  position = str(axis.get_position()).split()
  axis.close_device()

  return [position[1], position[3]]


def get_speed(address):
  axis = get_device(address)
  m = axis.get_move_settings()
  axis.close_device()

  return str(m.Speed)


def set_speed(address, speed):
  axis = get_device(address)
  m = axis.get_move_settings()
  m.Speed = speed
  axis.set_move_settings(m)
  axis.close_device()


def set_zero(address):
  axis = get_device(address)
  axis.command_zero()
  axis.close_device()


def get_edges(address):
  axis = get_device(address)
  edges = str(axis.get_edges_settings()).split()
  axis.close_device()

  return [edges[5], edges[9]]


def go_home(address):
  axis = get_device(address)
  axis.command_home()
  axis.command_wait_for_stop(stop)
  axis.close_device()


def move_to(address, position, microsteps):
  axis = get_device(address)
  axis.command_move(position, microsteps)
  axis.command_wait_for_stop(stop)
  axis.close_device()


def shift_on(address, steps, microsteps):
  axis = get_device(address)
  axis.command_movr(steps, microsteps)
  axis.command_wait_for_stop(stop)
  axis.close_device()


if __name__ == '__main__':
  shift_on(0, 10, 0)
  shift_on(0, -10, 0)
