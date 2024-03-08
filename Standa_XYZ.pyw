import os
import sys
import dat
import dev
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
    dat.Qbutton(self, self.linear, 'L', x, y - 50, m)
    dat.Qbutton(self, self.xin, 'X', x + 70, y - 50, m)
    dat.Qbutton(self, self.yin, 'Y', x + 120, y - 50, m)
    dat.Qbutton(self, self.zin, 'Z', x + 170, y - 50, m)
    dat.Qbutton(self, self.xout, 'X', x + 240, y - 50, m)
    dat.Qbutton(self, self.yout, 'Y', x + 290, y - 50, m)
    dat.Qbutton(self, self.zout, 'Z', x + 340, y - 50, m)
    dat.Qbutton(self, self.vertical, 'V', x + 410, y - 50, m)
    self.address = dat.Qedit(self, '', x, y, w)
    self.port = Standa.port[0]
    self.axis = Standa.device(self.port)
    self.steps = dat.Qedit(self, '10', x, y + 40, w)
    self.there = dat.Qedit(self, '', x, y + 80, w)
    self.position = dat.Qedit(self, '', x, y + 180, w)
    self.speed = dat.Qedit(self, '', x + w + 10, y + 180, w)
    dat.Qbutton(self, self.set_device, 'Set', x + w + 10, y, w)
    dat.Qbutton(self, self.shift_on, 'Shift on', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.move_to, 'Move to', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.set_zero, 'Set Zero', x, y + 120, w)
    dat.Qbutton(self, self.go_center, 'Center', x + w + 10, y + 120, w)
    dat.Qlabel(self, 'Position', x, y + 150, w)
    dat.Qlabel(self, 'Speed', x + w + 10, y + 150, w)

    self.linear()

    x, y, w = 240, 100, 100
    dat.Qbutton(self, self.p1, '+1', x, y - 40, w)
    dat.Qbutton(self, self.n1, '-1', x + w + 10, y - 40, w)
    dat.Qbutton(self, self.p10, '+10', x, y, w)
    dat.Qbutton(self, self.n10, '-10', x + w + 10, y, w)
    dat.Qbutton(self, self.p50, '+50', x, y + 40, w)
    dat.Qbutton(self, self.n50, '-50', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.p100, '+100', x, y + 80, w)
    dat.Qbutton(self, self.n100, '-100', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.p200, '+200', x, y + 120, w)
    dat.Qbutton(self, self.n200, '-200', x + w + 10, y + 120, w)
    dat.Qbutton(self, self.p500, '+500', x, y + 160, w)
    dat.Qbutton(self, self.n500, '-500', x + w + 10, y + 160, w)
    dat.Qbutton(self, self.p1000, '+1000', x, y + 200, w)
    dat.Qbutton(self, self.n1000, '-1000', x + w + 10, y + 200, w)

    x, y, w = 0, 300, 100
    dat.Qbutton(self, self.align, 'align', x, y, w)
    dat.Qbutton(self, self.scan_file_open, 'Open', x + w + 10, y, w)
    dat.Qbutton(self, self.operation, 'Operation', x, y + 40, w)
    dat.Qbutton(self, self.scan, 'Scan', x + w + 10, y + 40, w)

    self.data = np.array([])

  def get_device(self, n):
    self.port = n
    self.axis = Standa.device(Standa.port[n])
    self.address.setText(str(Standa.port[n]))
    self.speed.setText(Standa.get_speed(self.axis))
    self.there.setText(Standa.get_position(self.axis))
    self.position.setText(Standa.get_position(self.axis))

  def linear(self): self.get_device(0)

  def xin(self): self.get_device(1)
  def yin(self): self.get_device(2)
  def zin(self): self.get_device(3)

  def xout(self): self.get_device(4)
  def yout(self): self.get_device(5)
  def zout(self): self.get_device(6)

  def vertical(self): self.get_device(7)

  def set_device(self):
    steps = int(self.steps.text())
    speed = int(self.speed.text())

    Standa.set_speed(self.axis, speed)
    self.speed.setText(Standa.get_speed(self.axis))

    self.shift_steps(steps)
    self.shift_steps(-steps)

  def xyz(self, there):
    q, edge, f = Qw.QMessageBox, Standa.edge[self.port], True

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
    there = int(Standa.get_position(self.axis)) + steps
    if self.xyz(there):
      if abs(steps) > 500: Standa.set_speed(self.axis, 1000)
      Standa.shift_on(self.axis, there, 0)
      self.position.setText(Standa.get_position(self.axis))
      if abs(steps) > 500: Standa.set_speed(self.axis, 500)

  def move_to(self):
    there = int(self.there.text())
    position = int(Standa.get_position(self.axis))
    if self.xyz(there):
      if abs(there - position) > 500: Standa.set_speed(self.axis, 1000)
      Standa.move_to(self.axis, there, 0)
      self.position.setText(Standa.get_position(self.axis))
      if abs(there - position) > 500: Standa.set_speed(self.axis, 500)

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
      self.position.setText(Standa.get_position(self.axis))
      if abs(steps) > 500: Standa.set_speed(self.axis, 500)

  def p1(self): self.shift_steps(1)
  def n1(self): self.shift_steps(-1)
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
    self.axis = Standa.device(Standa.port[0])
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
      self.data = np.loadtxt(fp)
      print(self.data)

  def operation(self):
    if len(self.data):
      for step in self.data:
        self.shift_steps(int(step))
    else:
      print('None')

  def scan(self):
    pd = dev.Keysight_81630B_photodiode()
    pd.write('*CLS')
    pd.write('INIT1:CHAN1:CONT 0')
    pd.write('INIT1:CHAN1:IMM')

    dx, dp = [], []

    position = Standa.get_position(self.axis)
    Standa.shift_on(self.axis, -5, 0)
    for i in range(10):
      Standa.shift_on(self.axis, 1, 0)
      pwr = pd.read(1, 1)
      dx.append(i)
      dp.append(pwr)
      print(i, Standa.get_uposition(self.axis), pwr)
    Standa.move_to(self.axis, int(position), 0)
    print(Standa.get_uposition(self.axis))

    pd.write('INIT1:CHAN1:CONT 1')
    pd.close()

    plt.plot(dx, dp)
    plt.grid()
    plt.show()


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Motorized_Stages()
  window.show()
  sys.exit(app.exec_())
