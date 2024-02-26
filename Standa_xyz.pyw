import libximc.highlevel as ximc

dev_linear = r'xi-com:\\.\COM13'  # SN 32798 Axis 1
dev_vertical = r'xi-com:\\.\COM14'  # SN 32835 Axis 2


def Standa_8MT200_100(steps):
  axis = ximc.Axis(dev_linear)
  axis.open_device()
  m = axis.get_move_settings()
  m.Speed = 100
  axis.set_move_settings(m)
  axis.command_movr(steps, 0)
  axis.command_wait_for_stop(500)
  axis.command_movr(-steps, 0)
  axis.command_wait_for_stop(500)
  axis.command_stop()
  # print(axis.get_position())
  axis.close_device()


if __name__ == '__main__':
  Standa_8MT200_100(200)
