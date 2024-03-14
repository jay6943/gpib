import os
import sys
import dat
import Standa
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class Motorized_Stages(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.setWindowTitle('XYZ Scanning')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(1500, 200, 490, 490)

    x, y, w, m, s = 0, 60, 100, 40, 45
    dat.Qlabel(self, 'Input Axis', x + 70, y - 90, m * 3 + 20)
    dat.Qlabel(self, 'Output Axis', x + 240, y - 90, m * 3 + 20)
    dat.Qbutton(self, self.axis_linear, 'L', x, y - 50, m)
    dat.Qbutton(self, self.axis_xin, 'X', x + 70, y - 50, m)
    dat.Qbutton(self, self.axis_yin, 'Y', x + 120, y - 50, m)
    dat.Qbutton(self, self.axis_zin, 'Z', x + 170, y - 50, m)
    dat.Qbutton(self, self.axis_xout, 'X', x + 240, y - 50, m)
    dat.Qbutton(self, self.axis_yout, 'Y', x + 290, y - 50, m)
    dat.Qbutton(self, self.axis_zout, 'Z', x + 340, y - 50, m)
    dat.Qbutton(self, self.axis_vertical, 'V', x + 410, y - 50, m)
    self.addr = dat.Qedit(self, '', x, y, w)
    self.steps = dat.Qedit(self, '10', x, y + 40, s)
    self.micro_steps = dat.Qedit(self, '0', x + s + 5, y + 40, s)
    self.there = dat.Qedit(self, '', x, y + 80, s)
    self.micro_there = dat.Qedit(self, '', x + s + 5, y + 80, s)
    self.scan = dat.Qedit(self, '0', x, y + 200, s)
    self.micro_scan = dat.Qedit(self, '64', x + s + 5, y + 200, s)
    dat.Qbutton(self, self.set_device, 'Set', x + w + 10, y, w)
    dat.Qbutton(self, self.shift_on, 'Shift on', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.move_to, 'Move to', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.set_zero, 'Set Zero', x, y + 120, w)
    dat.Qbutton(self, self.go_center, 'Center', x + w + 10, y + 120, w)
    dat.Qbutton(self, self.find_max, 'Find Max', x + w + 10, y + 200, w)

    x, y, w = 240, 60, 100
    self.position = dat.Qedit(self, '', x, y, w)
    self.micro_position = dat.Qedit(self, '', x + w + 10, y, w)
    dat.Qbutton(self, self.p1, '+1', x, y + 40, w)
    dat.Qbutton(self, self.n1, '-1', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.p2, '+2', x, y + 80, w)
    dat.Qbutton(self, self.n2, '-2', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.p5, '+5', x, y + 120, w)
    dat.Qbutton(self, self.n5, '-5', x + w + 10, y + 120, w)
    dat.Qbutton(self, self.p10, '+10', x, y + 160, w)
    dat.Qbutton(self, self.n10, '-10', x + w + 10, y + 160, w)
    dat.Qbutton(self, self.p40, '+40', x, y + 200, w)
    dat.Qbutton(self, self.n40, '-40', x + w + 10, y + 200, w)
    dat.Qbutton(self, self.p100, '+100', x, y + 240, w)
    dat.Qbutton(self, self.n100, '-100', x + w + 10, y + 240, w)
    dat.Qbutton(self, self.p200, '+200', x, y + 280, w)
    dat.Qbutton(self, self.n200, '-200', x + w + 10, y + 280, w)
    dat.Qbutton(self, self.p500, '+500', x, y + 320, w)
    dat.Qbutton(self, self.n500, '-500', x + w + 10, y + 320, w)
    dat.Qbutton(self, self.p1000, '+1000', x, y + 360, w)
    dat.Qbutton(self, self.n1000, '-1000', x + w + 10, y + 360, w)

    x, y, w = 0, 380, 100
    dat.Qbutton(self, self.fiber_align, 'Fiber align', x, y, w)
    dat.Qbutton(self, self.chip_align, 'Chip align', x + w + 10, y, w)
    dat.Qbutton(self, self.scan_file, 'Open', x, y + 40, w)
    dat.Qbutton(self, self.operation, 'Operation', x + w + 10, y + 40, w)

    self.address = self.get_device(0)
    self.folder = dat.get_folder()
    self.align_data = []

  def get_device(self, address):
    axis = Standa.Stage(address)
    self.addr.setText(str(axis.port))
    position = axis.get_position()
    self.set_position(position)
    self.set_there(position)
    axis.close()

    return address

  def axis_linear(self): self.address = self.get_device(0)
  def axis_xin(self): self.address = self.get_device(1)
  def axis_yin(self): self.address = self.get_device(2)
  def axis_zin(self): self.address = self.get_device(3)
  def axis_xout(self): self.address = self.get_device(4)
  def axis_yout(self): self.address = self.get_device(5)
  def axis_zout(self): self.address = self.get_device(6)
  def axis_vertical(self): self.address = self.get_device(7)

  def set_device(self):
    self.shift_steps(10)
    self.shift_steps(-10)

  def set_position(self, position):
    self.position.setText(position[0])
    self.micro_position.setText(position[1])

  def set_there(self, there):
    self.there.setText(there[0])
    self.micro_there.setText(there[1])

  def set_scan_postision(self, position):
    self.scan.setText(position[0])
    self.micro_scan.setText(position[1])

  def get_edge(self, there):
    q, edge, f = Qw.QMessageBox, Standa.edge[self.address], True

    if abs(there) > edge:
      s = '최종 위치(' + str(there) + ') > 경계(' + str(edge) + ')'
      t = '경계까지 진행하시겠습니까?'
      a = q.question(self, 'Set Zero', s + ' ' + t, q.Yes | q.No, q.No)
      f = True if a == q.Yes else False

    return f

  def set_zero(self):
    axis = Standa.Stage(self.address)
    q = Qw.QMessageBox
    s = '현재 위치를 0으로 설정하시겠습니까?'
    a = q.question(self, 'Set Zero', s, q.Yes | q.No, q.No)
    if a == q.Yes: axis.set_zero()
    position = axis.get_position()
    self.set_there(position)
    self.set_position(position)
    axis.close()

  def shift_on(self):
    axis = Standa.Stage(self.address)
    steps = int(self.steps.text())
    if self.get_edge(int(axis.get_position()[0]) + steps):
      axis.shift_on(steps, int(self.micro_steps.text()))
      self.set_position(axis.get_position())
    axis.close()

  def move_to(self):
    axis = Standa.Stage(self.address)
    there = int(self.there.text())
    if self.get_edge(there):
      axis.move_to(there, int(self.micro_there.text()))
      self.set_position(axis.get_position())
    axis.close()

  def go_center(self):
    axis = Standa.Stage(self.address)
    axis.move_to(0, 0)
    self.set_position(axis.get_position())
    axis.close()

  def shift_steps(self, steps):
    axis = Standa.Stage(self.address)
    if self.get_edge(int(axis.get_position()[0]) + steps):
      axis.shift_on(steps, 0)
      self.set_position(axis.get_position())
    axis.close()

  def p1(self): self.shift_steps(1)
  def n1(self): self.shift_steps(-1)
  def p2(self): self.shift_steps(2)
  def n2(self): self.shift_steps(-2)
  def p5(self): self.shift_steps(5)
  def n5(self): self.shift_steps(-5)
  def p10(self): self.shift_steps(10)
  def n10(self): self.shift_steps(-10)
  def p40(self): self.shift_steps(40)
  def n40(self): self.shift_steps(-40)
  def p100(self): self.shift_steps(100)
  def n100(self): self.shift_steps(-100)
  def p200(self): self.shift_steps(200)
  def n200(self): self.shift_steps(-200)
  def p500(self): self.shift_steps(500)
  def n500(self): self.shift_steps(-500)
  def p1000(self): self.shift_steps(1000)
  def n1000(self): self.shift_steps(-1000)

  def chip_align(self):
    self.address = 0
    self.shift_steps(4162)
    self.shift_steps(-4162)
    print('Done.')

  def find_max(self):
    axis = Standa.Stage(self.address)
    steps = int(self.scan.text())
    micro = int(self.micro_scan.text())
    steps, micro, pwr = axis.find_max(steps, micro)
    self.set_position(axis.get_position())
    axis.close()

    print(Standa.title[self.address], end=' = ')
    print(str(pwr) + 'dBm at (' + steps + ', ' + micro + ')')

  def fiber_align(self):
    steps = int(self.scan.text())
    micro = int(self.micro_scan.text())
    max_power = -100
    for i in [2, 3, 5, 6]:
      print(Standa.title[i])
      axis = Standa.Stage(i)
      steps, micro, pwr = axis.find_max(steps, micro)
      if pwr > max_power: max_power = pwr
      axis.close()

    return max_power

  def operation(self):
    n, x, y = 2, [], []

    for i in range(n):
      x.append(round(0.4 - i * 0.02, 2))
      y.append(self.fiber_align())

      if i < n - 1:
        linear = Standa.Stage(0)
        linear.shift_on(40, 0)
        linear.close()

      print(np.array([x, y]).transpose())

      if i > 0:
        plt.figure(dpi=120)
        plt.plot(x, y)
        plt.xlabel('Tip width ($\mu$m)')
        plt.ylabel('Measured power (dBm)')
        plt.grid()
        plt.savefig('../data/scanning.png')
        plt.close()

  def scan_file(self):
    f = Qw.QFileDialog.getOpenFileName(self, '', dat.get_folder(), '*.txt')

    if f[0]:
      fp = open(f[0])
      data = fp.read()
      data = data.split('\n')
      self.align_data = []
      for i in range(len(data)):
        self.align_data.append(data[i].split(','))
        print(self.align_data[i])
      fp.close()

      self.folder = os.path.dirname(f[0])
      dat.set_folder(self.folder)

  def set_folder(self):
    cd = Qw.QFileDialog.getExistingDirectory(self, '', dat.get_folder())
    self.folder = cd
    dat.set_folder(self.folder)
    print(self.folder)


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Motorized_Stages()
  window.show()
  sys.exit(app.exec_())
