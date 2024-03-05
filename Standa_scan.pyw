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
    self.setGeometry(500, 500, 420, 300)

    self.linear = Standa.device('5')

    self.inx = Standa.device('12')
    self.iny = Standa.device('10')
    self.inz = Standa.device('14')

    self.outx = Standa.device('11')
    self.outy = Standa.device('9')
    self.outz = Standa.device('13')

    self.inz_home = 320

    dat.Qbutton(self, self.linear_shift_on, 'Linear', 0, 0, 120)
    dat.Qbutton(self, self.linear_move_to, 'Move to', 130, 0, 120)
    dat.Qbutton(self, self.linear_test, 'Test', 260, 0, 120)
    self.l_steps = dat.Qedit(self, '500', 0, 40, 120)
    self.l_position = dat.Qedit(self, '', 130, 40, 120)
    self.l_speed = dat.Qedit(self, '', 260, 40, 120)
    dat.Qlabel(self, Standa.get_edges(self.linear), 10, 70, 200)

    self.l_position.setText(Standa.get_position(self.laxis))
    self.l_speed.setText(Standa.get_speed(self.vaxis))

    dat.Qlabel(self, 'COM', 10, 270, 30)
    self.address = dat.Qedit(self, '14', 40, 280, 80)
    self.axis = Standa.device(self.address.text())

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
