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
    self.setGeometry(500, 500, 420, 500)

    self.laxis = Standa.device('5')
    self.vaxis = Standa.device('15')

    dat.Qbutton(self, self.linear_shift_on, 'Linear', 0, 0, 120)
    dat.Qbutton(self, self.linear_move_to, 'Move to', 130, 0, 120)
    dat.Qbutton(self, self.linear_test, 'Test', 260, 0, 120)
    self.l_steps = dat.Qedit(self, '500', 0, 40, 120)
    self.l_position = dat.Qedit(self, '', 130, 40, 120)
    self.l_speed = dat.Qedit(self, '', 260, 40, 120)
    dat.Qlabel(self, Standa.get_edges(self.laxis), 10, 70, 200)

    dat.Qbutton(self, self.vertical_shift_on, 'Vertical', 0, 120, 120)
    dat.Qbutton(self, self.vertical_move_to, 'Move to', 130, 120, 120)
    dat.Qbutton(self, self.vertical_test, 'Test', 260, 120, 120)
    self.v_steps = dat.Qedit(self, '50', 0, 160, 120)
    self.v_position = dat.Qedit(self, '', 130, 160, 120)
    self.v_speed = dat.Qedit(self, '', 260, 160, 120)
    dat.Qlabel(self, Standa.get_edges(self.vaxis), 10, 190, 200)
    dat.Qbutton(self, self.vertical_home, 'Home', 260, 200, 120)

    self.l_position.setText(Standa.get_position(self.laxis))
    self.v_position.setText(Standa.get_position(self.vaxis))
    self.l_speed.setText(Standa.get_speed(self.laxis))
    self.v_speed.setText(Standa.get_speed(self.vaxis))

    self.address = dat.Qedit(self, '13', 0, 280, 120)
    self.axis = Standa.device(self.address.text())

    dat.Qbutton(self, self.axis_get_device, 'COM', 130, 280, 120)
    dat.Qbutton(self, self.axis_shift_on, 'Shift on', 0, 320, 120)
    dat.Qbutton(self, self.axis_move_to, 'Move to', 130, 320, 120)
    dat.Qbutton(self, self.axis_test, 'Test', 260, 320, 120)
    self.axis_steps = dat.Qedit(self, '50', 0, 360, 120)
    self.axis_position = dat.Qedit(self, '', 130, 360, 120)
    self.axis_speed = dat.Qedit(self, '', 260, 360, 120)
    dat.Qlabel(self, Standa.get_edges(self.axis), 10, 390, 200)
    dat.Qbutton(self, self.axis_home, 'Home', 260, 400, 120)

    self.axis_position.setText(Standa.get_position(self.axis))
    self.axis_speed.setText(Standa.get_speed(self.axis))

  def linear_shift_on(self):
    Standa.shift_on(self.laxis, int(self.l_steps.text()), 0)
    self.l_position.setText(Standa.get_position(self.laxis))

  def linear_move_to(self):
    Standa.move_to(self.laxis, int(self.l_position.text()), 0)
    self.l_position.setText(Standa.get_position(self.laxis))

  def linear_test(self):
    steps = int(self.l_steps.text())
    speed = int(self.l_speed.text())

    Standa.set_speed(self.laxis, speed)
    Standa.shift_on(self.laxis, steps, 0)
    Standa.shift_on(self.laxis, -steps, 0)
    self.l_position.setText(Standa.get_position(self.laxis))

  def vertical_shift_on(self):
    Standa.shift_on(self.vaxis, int(self.v_steps.text()), 0)
    self.v_position.setText(Standa.get_position(self.vaxis))

  def vertical_move_to(self):
    Standa.move_to(self.vaxis, int(self.v_position.text()), 0)
    self.v_position.setText(Standa.get_position(self.vaxis))

  def vertical_test(self):
    steps = int(self.v_steps.text())
    speed = int(self.v_speed.text())

    Standa.set_speed(self.vaxis, speed)
    Standa.shift_on(self.vaxis, steps, 0)
    Standa.shift_on(self.vaxis, -steps, 0)
    self.v_position.setText(Standa.get_position(self.vaxis))

  def vertical_home(self):
    Standa.go_home(self.vaxis)
    self.v_position.setText(Standa.get_position(self.vaxis))

  def axis_get_device(self):
    self.axis = Standa.device(self.address.text())
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_shift_on(self):
    Standa.shift_on(self.axis, int(self.axis_steps.text()), 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_move_to(self):
    Standa.move_to(self.axis, int(self.axis_position.text()), 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_test(self):
    steps = int(self.axis_steps.text())
    speed = int(self.axis_speed.text())

    Standa.set_speed(self.axis, speed)
    Standa.shift_on(self.axis, steps, 0)
    Standa.shift_on(self.axis, -steps, 0)
    self.axis_position.setText(Standa.get_position(self.axis))

  def axis_home(self):
    Standa.go_home(self.axis)
    self.axis_position.setText(Standa.get_position(self.axis))


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
