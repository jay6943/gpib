import sys
import dat
import Standa
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw


class motors(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.setWindowTitle('Standa XYZ')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(3500, 500, 420, 490)

    x, y, w, m = 0, 60, 100, 40
    dat.Qlabel(self, 'Input Axis', x + 70, y - 90, w)
    dat.Qlabel(self, 'Output Axis', x + 240, y - 90, w)
    dat.Qbutton(self, self.linear, 'L', x, y - 50, m)
    dat.Qbutton(self, self.xin, 'X', x + 70, y - 50, m)
    dat.Qbutton(self, self.yin, 'Y', x + 120, y - 50, m)
    dat.Qbutton(self, self.zin, 'Z', x + 170, y - 50, m)
    dat.Qbutton(self, self.xout, 'X', x + 240, y - 50, m)
    dat.Qbutton(self, self.yout, 'Y', x + 290, y - 50, m)
    dat.Qbutton(self, self.zout, 'Z', x + 340, y - 50, m)
    self.address = dat.Qedit(self, '', x, y, w)
    self.port = Standa.port[0]
    self.axis = Standa.device(self.port)
    self.steps = dat.Qedit(self, '10', x, y + 40, w)
    self.there = dat.Qedit(self, '', x, y + 80, w)
    self.position = dat.Qedit(self, '', x, y + 180, w)
    self.speed = dat.Qedit(self, '', x + w + 10, y + 180, w)
    self.amin = dat.Qedit(self, '', x, y + 240, w)
    self.amax = dat.Qedit(self, '', x + w + 10, y + 240, w)
    dat.Qbutton(self, self.set_device, 'Set', x + w + 10, y, w)
    dat.Qbutton(self, self.shift_on, 'Shift on', x + w + 10, y + 40, w)
    dat.Qbutton(self, self.move_to, 'Move to', x + w + 10, y + 80, w)
    dat.Qbutton(self, self.go_center, 'Home', x + w + 10, y + 120, w)
    dat.Qlabel(self, 'Position', x, y + 150, w)
    dat.Qlabel(self, 'Speed', x + w + 10, y + 150, w)
    dat.Qlabel(self, 'Min', x, y + 210, w)
    dat.Qlabel(self, 'Max', x + w + 10, y + 210, w)

    x, y, w = 0, 360, 100
    dat.Qbutton(self, self.align, 'align', x, y, w)

    x, y, w = 240, 100, 65
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

    self.linear()

  def get_device(self, n):
    self.port = n
    self.axis = Standa.device(Standa.port[n])
    self.address.setText(str(Standa.port[n]))
    self.there.setText(str(int((Standa.amax[n] + Standa.amin[n]) / 2)))
    self.speed.setText(Standa.get_speed(self.axis))
    self.position.setText(Standa.get_position(self.axis))
    self.amin.setText(str(Standa.amin[n]))
    self.amax.setText(str(Standa.amax[n]))

  def linear(self): self.get_device(0)

  def xin(self): self.get_device(1)
  def yin(self): self.get_device(2)
  def zin(self): self.get_device(3)

  def xout(self): self.get_device(4)
  def yout(self): self.get_device(5)
  def zout(self): self.get_device(6)

  def set_device(self):
    steps = int(self.steps.text())
    speed = int(self.speed.text())

    Standa.set_speed(self.axis, speed)
    Standa.shift_on(self.axis, steps, 0)
    Standa.shift_on(self.axis, -steps, 0)
    self.position.setText(Standa.get_position(self.axis))

  def shift_on(self):
    Standa.shift_on(self.axis, int(self.steps.text()), 0)
    self.position.setText(Standa.get_position(self.axis))

  def move_to(self):
    Standa.move_to(self.axis, int(self.there.text()), 0)
    self.position.setText(Standa.get_position(self.axis))

  def go_home(self):
    Standa.go_home(self.axis)
    self.position.setText(Standa.get_position(self.axis))

  def go_center(self):
    Standa.go_center(self.axis, self.port)
    self.position.setText(Standa.get_position(self.axis))

  def shift_steps(self, steps):
    Standa.shift_on(self.axis, steps, 0)
    self.position.setText(Standa.get_position(self.axis))

  def align(self):
    self.shift_steps(4162)
    self.shift_steps(-4162)

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


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
