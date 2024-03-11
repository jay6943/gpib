import os
import sys
import dat
import dev
import time
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
    self.setGeometry(2800, 500, 490, 490)

    x, y, w, m = 0, 60, 100, 40
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
    self.address = dat.Qedit(self, '', x, y, w)
    self.steps = dat.Qedit(self, '10', x, y + 40, w)
    self.there = dat.Qedit(self, '', x, y + 80, w)
    self.scan = dat.Qedit(self, '1', x, y + 200, w)
    self.amax = dat.Qedit(self, '', x, y + 240, w)
    dat.Qbutton(self, self.set_device, 'Set', x + w + 10, y, w)
    dat.Qbutton(self, self.shift_on, 'Shift on', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.move_to, 'Move to', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.set_zero, 'Set Zero', x, y + 120, w)
    dat.Qbutton(self, self.go_center, 'Center', x + w + 10, y + 120, w)
    dat.Qbutton(self, self.scanning, 'Scan', x + w + 10, y + 200, w)
    dat.Qbutton(self, self.to_max, 'to Max', x + w + 10, y + 240, w)

    x, y, w = 240, 60, 100
    dat.Qlabel(self, 'Position', x, y - 30, w)
    dat.Qlabel(self, 'Speed', x + w + 10, y - 30, w)
    self.position = dat.Qedit(self, '', x, y, w)
    self.speed = dat.Qedit(self, '', x + w + 10, y, w)
    dat.Qbutton(self, self.p1, '+1', x, y + 40, w)
    dat.Qbutton(self, self.n1, '-1', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.p2, '+2', x, y + 80, w)
    dat.Qbutton(self, self.n2, '-2', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.p5, '+5', x, y + 120, w)
    dat.Qbutton(self, self.n5, '-5', x + w + 10, y + 120, w)
    dat.Qbutton(self, self.p10, '+10', x, y + 160, w)
    dat.Qbutton(self, self.n10, '-10', x + w + 10, y + 160, w)
    dat.Qbutton(self, self.p50, '+50', x, y + 200, w)
    dat.Qbutton(self, self.n50, '-50', x + w + 10, y + 200, w)
    dat.Qbutton(self, self.p100, '+100', x, y + 240, w)
    dat.Qbutton(self, self.n100, '-100', x + w + 10, y + 240, w)
    dat.Qbutton(self, self.p200, '+200', x, y + 280, w)
    dat.Qbutton(self, self.n200, '-200', x + w + 10, y + 280, w)
    dat.Qbutton(self, self.p500, '+500', x, y + 320, w)
    dat.Qbutton(self, self.n500, '-500', x + w + 10, y + 320, w)
    dat.Qbutton(self, self.p1000, '+1000', x, y + 360, w)
    dat.Qbutton(self, self.n1000, '-1000', x + w + 10, y + 360, w)

    x, y, w = 0, 380, 100
    dat.Qbutton(self, self.scan_file_open, 'Open', x, y, w)
    dat.Qbutton(self, self.operation, 'Operation', x + w + 10, y, w)
    dat.Qbutton(self, self.align, 'align', x + w + 10, y + 40, w)

    self.max1 = ''
    self.max2 = ''
    self.axis = 0
    self.data = []

  def get_device(self, axis):
    self.axis = axis
    self.address.setText(str(Standa.port[axis]))
    self.speed.setText(Standa.get_speed(axis))
    self.position.setText(Standa.get_position(axis))
    self.there.setText('')
    if axis < 4: self.amax.setText(str(self.max1))
    else: self.amax.setText(str(self.max2))

  def axis_linear(self): self.get_device(0)
  def axis_xin(self): self.get_device(1)
  def axis_yin(self): self.get_device(2)
  def axis_zin(self): self.get_device(3)
  def axis_xout(self): self.get_device(4)
  def axis_yout(self): self.get_device(5)
  def axis_zout(self): self.get_device(6)
  def axis_vertical(self): self.get_device(7)

  def set_device(self):
    steps = int(self.steps.text())
    speed = int(self.speed.text())

    Standa.set_speed(self.axis, speed)
    self.speed.setText(Standa.get_speed(self.axis))

    self.shift_steps(steps)
    self.shift_steps(-steps)

  def xyz(self, there):
    q, edge, f = Qw.QMessageBox, Standa.edge[self.axis], True

    if abs(there) > edge:
      s = '최종 위치(' + str(there) + ')가 경계(' + str(edge) + ')보다 큽니다.'
      t = '경계까지 진행하시겠습니까?'
      a = q.question(self, 'Set Zero', s + ' ' + t, q.Yes | q.No, q.No)
      f = True if a == q.Yes else False

    return f

  def set_zero(self):
    q = Qw.QMessageBox
    s = '현재 위치를 0으로 설정하시겠습니까?'
    a = q.question(self, 'Set Zero', s, q.Yes | q.No, q.No)
    if a == q.Yes: Standa.set_zero(self.axis)
    position = Standa.get_position(self.axis)
    self.there.setText(position)
    self.position.setText(position)

  def shift_on(self):
    steps = int(self.steps.text())
    if self.xyz(int(Standa.get_position(self.axis)) + steps):
      Standa.shift_on(self.axis, steps, 0)
      self.position.setText(Standa.get_position(self.axis))

  def move_to(self):
    there = int(self.there.text())
    if self.xyz(there):
      Standa.move_to(self.axis, there, 0)
      self.position.setText(Standa.get_position(self.axis))

  def to_max(self):
    there = int(self.amax.text())
    if self.xyz(there):
      Standa.move_to(self.axis, there, 0)
      self.position.setText(Standa.get_position(self.axis))

  def go_center(self):
    self.shift_steps(-int(Standa.get_position(self.axis)))
    self.speed.setText(Standa.get_speed(self.axis))
    self.position.setText(Standa.get_position(self.axis))

  def shift_steps(self, steps):
    there = int(Standa.get_position(self.axis)) + steps
    if self.xyz(there):
      if abs(steps) > 500: Standa.set_speed(self.axis, 1000)
      if abs(steps) > 2000: Standa.set_speed(self.axis, 2000)
      Standa.shift_on(self.axis, steps, 0)
      Standa.set_speed(self.axis, 500)
      self.position.setText(Standa.get_position(self.axis))

  def p1(self): self.shift_steps(1)
  def n1(self): self.shift_steps(-1)
  def p2(self): self.shift_steps(2)
  def n2(self): self.shift_steps(-2)
  def p5(self): self.shift_steps(5)
  def n5(self): self.shift_steps(-5)
  def p10(self): self.shift_steps(10)
  def n10(self): self.shift_steps(-10)
  def p50(self): self.shift_steps(50)
  def n50(self): self.shift_steps(-50)
  def p100(self): self.shift_steps(100)
  def n100(self): self.shift_steps(-100)
  def p200(self): self.shift_steps(200)
  def n200(self): self.shift_steps(-200)
  def p500(self): self.shift_steps(500)
  def n500(self): self.shift_steps(-500)
  def p1000(self): self.shift_steps(1000)
  def n1000(self): self.shift_steps(-1000)

  def align(self):
    self.axis = 0
    Standa.set_speed(self.axis, 2000)
    self.shift_steps(4162)
    self.shift_steps(-4162)
    Standa.set_speed(self.axis, 500)
    self.speed.setText(Standa.get_speed(self.axis))

  def scan_file_open(self):
    fp = Qw.QFileDialog.getOpenFileName(self, '', dat.get_folder(), '*.txt')[0]
    cd = os.path.dirname(fp)

    if fp:
      dat.set_folder(cd)
      self.data = np.loadtxt(fp, delimiter=',')
      print(self.data)

  def operation(self):
    pd = dev.Keysight_81630B_photodiode()
    pd.write('*CLS')
    pd.write('INIT1:CHAN1:CONT 0')
    pd.write('INIT1:CHAN1:IMM')

    for axis in self.data:
      Standa.move_to(0, int(axis[0]), 0)
      Standa.move_to(2, int(axis[1]), 0)
      Standa.move_to(3, int(axis[2]), 0)
      Standa.move_to(5, int(axis[3]), 0)
      Standa.move_to(6, int(axis[4]), 0)
      time.sleep(1000)

      print(axis, pd.read(1, 1))

    pd.write('INIT1:CHAN1:CONT 1')
    pd.close()

  def scanning(self):
    pd = dev.Keysight_81630B_photodiode()
    pd.write('*CLS')
    pd.write('INIT1:CHAN1:CONT 0')
    pd.write('INIT1:CHAN1:IMM')

    dx, dp = [], []

    n = 10
    steps = int(self.scan.text())
    position = int(Standa.get_position(self.axis))
    Standa.shift_on(self.axis, -steps * n, 0)
    for i in range(n * 2):
      Standa.shift_on(self.axis, steps, 0)
      there = int(Standa.get_position(self.axis))
      pwr = pd.read(1, 1)
      dx.append(there)
      dp.append(pwr)
      print(i, Standa.get_uposition(self.axis), pwr)
    Standa.move_to(self.axis, position, 0)
    self.amax.setText(str(dx[dp.index(max(dp))]))

    pd.write('INIT1:CHAN1:CONT 1')
    pd.close()

    plt.figure(dpi=120)
    plt.plot(dx, dp)
    plt.xlabel('Axis position')
    plt.ylabel('Measured power (dBm)')
    plt.grid()
    plt.savefig('../data/scanning.png')
    plt.show()

  def scanning_2D(self):
    axis1 = self.axis
    axis2 = self.axis + 3

    pd = dev.Keysight_81630B_photodiode()
    pd.write('*CLS')
    pd.write('INIT1:CHAN1:CONT 0')
    pd.write('INIT1:CHAN1:IMM')

    dx1, dx2, dp = [], [], []

    n = 10
    steps = int(self.scan.text())
    position1 = int(Standa.get_position(axis1))
    Standa.shift_on(axis1, -steps * n, 0)
    position2 = int(Standa.get_position(axis2))
    Standa.shift_on(axis2, -steps * n, 0)
    for i in range(n * 2):
      Standa.shift_on(axis1, steps, 0)
      there1 = int(Standa.get_position(axis1))
      Standa.shift_on(axis2, steps, 0)
      there2 = int(Standa.get_position(axis2))
      pwr = pd.read(1, 1)
      dx1.append(there1)
      dx2.append(there2)
      dp.append(pwr)
      print(i, there1, there2, pwr)
    Standa.move_to(axis1, position1, 0)
    Standa.move_to(axis2, position2, 0)
    self.amax.setText(str(dx1[dp.index(max(dp))]))
    self.max1 = dx1[dp.index(max(dp))]
    self.max2 = dx2[dp.index(max(dp))]
    print(self.max1, self.max2)

    pd.write('INIT1:CHAN1:CONT 1')
    pd.close()

    plt.figure(dpi=120)
    plt.plot(dx1, dp)
    plt.xlabel('Axis position')
    plt.ylabel('Measured power (dBm)')
    plt.grid()
    plt.savefig('../data/scanning.png')
    plt.close()

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Motorized_Stages()
  window.show()
  sys.exit(app.exec_())
