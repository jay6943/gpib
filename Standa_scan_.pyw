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
    self.setGeometry(3500, 500, 570, 490)

    xp, yp = 0, 50
    dat.Qbutton(self, self.xin, 'L', xp, yp-40, 40)
    self.l_address = dat.Qedit(self, '5', xp, yp, 100)
    self.linear = Standa.device(int(self.l_address.text()))
    self.l_steps = dat.Qedit(self, '50', xp, yp+40, 100)
    self.l_there = dat.Qedit(self, '', xp, yp+80, 100)
    self.l_position = dat.Qedit(self, '', xp, yp+180, 100)
    self.l_speed = dat.Qedit(self, '', xp+110, yp+180, 100)
    self.l_min = dat.Qedit(self, '', xp, yp+240, 100)
    self.l_max = dat.Qedit(self, '', xp+110, yp+240, 100)
    dat.Qbutton(self, self.linear_init, 'Linear', xp+110, yp, 100)
    dat.Qbutton(self, self.linear_shift_on, 'Shift on', xp+110, yp+40, 100)
    dat.Qbutton(self, self.linear_move_to, 'Move to', xp + 110, yp+80, 100)
    dat.Qbutton(self, self.linear_home, 'Home', xp+150, yp+120, 140)
    dat.Qlabel(self, 'Position', xp, yp+150, 100)
    dat.Qlabel(self, 'Speed', xp+110, yp+150, 100)
    dat.Qlabel(self, 'Min', xp, yp+210, 100)
    dat.Qlabel(self, 'Max', xp+110, yp+210, 100)
    self.l_position.setText(Standa.get_position(self.linear))
    self.l_there.setText(Standa.get_position(self.linear))
    self.l_speed.setText(Standa.get_speed(self.linear))
    self.l_min.setText(Standa.get_edges(self.linear)[0])
    self.l_max.setText(Standa.get_edges(self.linear)[1])

    xp, yp = 240, 50
    dat.Qlabel(self, 'Input Axis', xp, yp-80, 140)
    dat.Qlabel(self, 'Output Axis', xp+150, yp-80, 140)
    dat.Qbutton(self, self.xin, 'X', xp, yp-40, 40)
    dat.Qbutton(self, self.yin, 'Y', xp+50, yp-40, 40)
    dat.Qbutton(self, self.zin, 'Z', xp+100, yp-40, 40)
    dat.Qbutton(self, self.xout, 'X', xp+150, yp-40, 40)
    dat.Qbutton(self, self.yout, 'Y', xp+200, yp-40, 40)
    dat.Qbutton(self, self.zout, 'Z', xp+250, yp-40, 40)
    self.axis_address = dat.Qedit(self, '14', xp, yp, 140)
    self.axis = Standa.device(int(self.axis_address.text()))
    self.axis_steps = dat.Qedit(self, '50', xp, yp+40, 140)
    self.axis_there = dat.Qedit(self, '', xp, yp+80, 140)
    self.axis_position = dat.Qedit(self, '', xp, yp+180, 140)
    self.axis_speed = dat.Qedit(self, '', xp+150, yp+180, 140)
    self.axis_min = dat.Qedit(self, '', xp, yp+240, 140)
    self.axis_max = dat.Qedit(self, '', xp+150, yp+240, 140)
    dat.Qbutton(self, self.axis_init, 'Axis', xp+150, yp, 140)
    dat.Qbutton(self, self.axis_shift_on, 'Shift on', xp+150, yp+40, 140)
    dat.Qbutton(self, self.axis_move_to, 'Move to', xp+150, yp+80, 140)
    dat.Qbutton(self, self.axis_home, 'Home', xp+150, yp+120, 140)
    dat.Qlabel(self, 'Position', xp, yp+150, 140)
    dat.Qlabel(self, 'Speed', xp+150, yp+150, 140)
    dat.Qlabel(self, 'Min', xp, yp+210, 140)
    dat.Qlabel(self, 'Max', xp+150, yp+210, 140)

    xp, yp = 245, 340
    dat.Qbutton(self, self.p10, '+10', xp, yp, 60)
    dat.Qbutton(self, self.n10, '-10', xp+70, yp, 60)
    dat.Qbutton(self, self.p50, '+50', xp+150, yp, 60)
    dat.Qbutton(self, self.n50, '-50', xp+220, yp, 60)
    dat.Qbutton(self, self.p100, '+100', xp, yp+40, 60)
    dat.Qbutton(self, self.n100, '-100', xp+70, yp+40, 60)
    dat.Qbutton(self, self.p200, '+200', xp+150, yp+40, 60)
    dat.Qbutton(self, self.n200, '-200', xp+220, yp+40, 60)
    dat.Qbutton(self, self.p500, '+500', xp, yp+80, 60)
    dat.Qbutton(self, self.n500, '-500', xp+70, yp+80, 60)
    dat.Qbutton(self, self.p1000, '+1000', xp+150, yp+80, 60)
    dat.Qbutton(self, self.n1000, '-1000', xp+220, yp+80, 60)

  def linear_init(self):
    steps = int(self.l_steps.text())
    speed = int(self.l_speed.text())

    Standa.set_speed(self.linear, speed)
    Standa.shift_on(self.linear, steps, 0)
    Standa.shift_on(self.linear, -steps, 0)
    self.l_position.setText(Standa.get_position(self.linear))

  def linear_shift_on(self):
    Standa.shift_on(self.linear, int(self.l_steps.text()), 0)
    self.l_position.setText(Standa.get_position(self.linear))

  def linear_move_to(self):
    Standa.move_to(self.linear, int(self.l_there.text()), 0)
    self.l_position.setText(Standa.get_position(self.linear))

  def linear_home(self):
    there = (Standa.pmax[0] + Standa.pmin[0]) / 2
    Standa.move_to(self.linear, int(there), 0)
    self.l_position.setText(Standa.get_position(self.linear))

  def get_device(self, idev):
    self.axis = Standa.device(Standa.port[idev])
    self.axis_address.setText(str(Standa.port[idev]))
    self.axis_there.setText(str(Standa.home[idev]))
    self.axis_speed.setText(Standa.get_speed(self.axis))
    self.axis_position.setText(Standa.get_position(self.axis))
    self.axis_min.setText(str(Standa.pmin[idev]))
    self.axis_max.setText(str(Standa.pmax[idev]))

  def xin(self): self.get_device(1)
  def yin(self): self.get_device(2)
  def zin(self): self.get_device(3)

  def xout(self): self.get_device(4)
  def yout(self): self.get_device(5)
  def zout(self): self.get_device(6)

  def axis_init(self):
    steps = int(self.axis_steps.text())
    speed = int(self.axis_speed.text())

    Standa.set_speed(self.axis, speed)
    Standa.shift_on(self.axis, steps, 0)
    Standa.shift_on(self.axis, -steps, 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_shift_on(self):
    Standa.shift_on(self.axis, int(self.axis_steps.text()), 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_move_to(self):
    Standa.move_to(self.axis, int(self.axis_there.text()), 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_home(self):
    Standa.go_home(self.axis)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_shift_steps(self, steps):
    Standa.shift_on(self.axis, steps, 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def p10(self): self.axis_shift_steps(10)
  def n10(self): self.axis_shift_steps(-10)
  def p50(self): self.axis_shift_steps(50)
  def n50(self): self.axis_shift_steps(-50)
  def p100(self): self.axis_shift_steps(100)
  def n100(self): self.axis_shift_steps(-100)
  def p200(self): self.axis_shift_steps(200)
  def n200(self): self.axis_shift_steps(-200)
  def p500(self): self.axis_shift_steps(500)
  def n500(self): self.axis_shift_steps(-500)
  def p1000(self): self.axis_shift_steps(1000)
  def n1000(self): self.axis_shift_steps(-1000)


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
