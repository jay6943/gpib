import time
import libximc.highlevel as ximc

dev_linear = r'xi-com:\\.\COM13'  # SN 32798 Axis 1
dev_vertical = r'xi-com:\\.\COM14'  # SN 32835 Axis 2
# dev_x1 = r'xi-com:\\.\COM9'  # SN 32800 Axis 1
# dev_y1 = r'xi-com:\\.\COM10'  # SN 32776 Axis 2
# dev_z1 = r'xi-com:\\.\COM5'  # SN
# dev_z2 = r'xi-com:\\.\COM15'  # SN


def get_info(device):
  axis = ximc.Axis(device)
  axis.open_device()
  sn = str(axis.get_serial_number())
  sf = 'Status\n\n' + str(axis.get_status()) + '\n'
  df = 'Move settings\n\n' + str(axis.get_move_settings()) + '\n'
  cf = 'Control settings\n\n' + str(axis.get_engine_settings()) + '\n'
  mf = 'Motor settings\n\n' + str(axis.get_engine_settings()) + '\n'
  axis.close_device()

  fp = open('../data/Standa_' + sn + '.txt', 'w')
  data = str(device) + '\n' + sn + '\n\n' + sf + df + cf + mf
  fp.write(data)
  fp.close()


def Standa_time():
  axis = ximc.Axis(dev_linear)
  axis.open_device()
  axis.command_right()
  time.sleep(3)
  axis.command_stop()
  axis.close_device()


def Standa_8MT200_100():
  axis = ximc.Axis(dev_linear)
  axis.open_device()
  axis.command_movr(10, 0)
  axis.command_wait_for_stop(500)
  # axis.command_movr(-100, 0)
  # axis.command_wait_for_stop(500)
  df = str(axis.get_position())
  axis.command_stop()
  axis.close_device()

  df = df.split()

  print(df)


def Standa_8MVT70_13_1():
  axis = ximc.Axis(dev_vertical)
  axis.open_device()
  axis.command_home()
  axis.command_wait_for_stop(500)
  # axis.command_right()
  # time.sleep(1)
  axis.command_stop()
  axis.close_device()


if __name__ == '__main__':
  Standa_8MT200_100()
  # Standa_8MVT70_13_1()

  # get_info(dev_linear)
  # get_info(dev_vertical)
