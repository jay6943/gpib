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
    self.setGeometry(3500, 500, 730, 310)

    self.l_address = dat.Qedit(self, '5', 0, 0, 100)
    self.linear = Standa.device(self.l_address.text())
    self.l_steps = dat.Qedit(self, '50', 0, 40, 100)
    self.l_there = dat.Qedit(self, '', 0, 80, 100)
    self.l_position = dat.Qedit(self, '', 0, 180, 100)
    self.l_speed = dat.Qedit(self, '', 110, 180, 100)
    self.l_min = dat.Qedit(self, '', 0, 240, 100)
    self.l_max = dat.Qedit(self, '', 110, 240, 100)
    dat.Qbutton(self, self.linear_init, 'Linear', 110, 0, 100)
    dat.Qbutton(self, self.linear_shift_on, 'Shift on', 110, 40, 100)
    dat.Qbutton(self, self.linear_move_to, 'Move to', 110, 80, 100)
    dat.Qlabel(self, 'Position', 0, 150, 100)
    dat.Qlabel(self, 'Speed', 110, 150, 100)
    dat.Qlabel(self, 'Min', 0, 210, 100)
    dat.Qlabel(self, 'Max', 110, 210, 100)
    self.l_position.setText(Standa.get_position(self.linear))
    self.l_there.setText(Standa.get_position(self.linear))
    self.l_speed.setText(Standa.get_speed(self.linear))
    self.l_min.setText(Standa.get_edges(self.linear)[0])
    self.l_max.setText(Standa.get_edges(self.linear)[1])

    self.v_address = dat.Qedit(self, '15', 240, 0, 100)
    self.vertical = Standa.device(self.v_address.text())
    self.v_steps = dat.Qedit(self, '50', 240, 40, 100)
    self.v_there = dat.Qedit(self, '', 240, 80, 100)
    self.v_position = dat.Qedit(self, '', 240, 180, 100)
    self.v_speed = dat.Qedit(self, '', 350, 180, 100)
    self.v_min = dat.Qedit(self, '', 240, 240, 100)
    self.v_max = dat.Qedit(self, '', 350, 240, 100)
    dat.Qbutton(self, self.vertical_init, 'Vertical', 350, 0, 100)
    dat.Qbutton(self, self.vertical_shift_on, 'Shift on', 350, 40, 100)
    dat.Qbutton(self, self.vertical_move_to, 'Move to', 350, 80, 100)
    dat.Qbutton(self, self.vertical_home, 'Home', 350, 120, 100)
    dat.Qlabel(self, 'Position', 240, 150, 100)
    dat.Qlabel(self, 'Speed', 350, 150, 100)
    dat.Qlabel(self, 'Min', 240, 210, 100)
    dat.Qlabel(self, 'Max', 350, 210, 100)
    self.v_position.setText(Standa.get_position(self.vertical))
    self.v_there.setText(Standa.get_position(self.vertical))
    self.v_speed.setText(Standa.get_speed(self.vertical))
    self.v_min.setText(Standa.get_edges(self.vertical)[0])
    self.v_max.setText(Standa.get_edges(self.vertical)[1])

    self.axis_address = dat.Qedit(self, '14', 480, 0, 100)
    self.axis = Standa.device(self.axis_address.text())
    self.axis_steps = dat.Qedit(self, '50', 480, 40, 100)
    self.axis_there = dat.Qedit(self, '', 480, 80, 100)
    self.axis_position = dat.Qedit(self, '', 480, 180, 100)
    self.axis_speed = dat.Qedit(self, '', 590, 180, 100)
    self.axis_min = dat.Qedit(self, '', 480, 240, 100)
    self.axis_max = dat.Qedit(self, '', 590, 240, 100)
    dat.Qbutton(self, self.axis_init, 'Axis', 590, 0, 100)
    dat.Qbutton(self, self.axis_shift_on, 'Shift on', 590, 40, 100)
    dat.Qbutton(self, self.axis_move_to, 'Move to', 590, 80, 100)
    dat.Qbutton(self, self.axis_home, 'Home', 590, 120, 100)
    dat.Qlabel(self, 'Position', 480, 150, 100)
    dat.Qlabel(self, 'Speed', 590, 150, 100)
    dat.Qlabel(self, 'Min', 480, 210, 100)
    dat.Qlabel(self, 'Max', 590, 210, 100)
    self.axis_position.setText(Standa.get_position(self.axis))
    self.axis_there.setText(Standa.get_position(self.axis))
    self.axis_speed.setText(Standa.get_speed(self.axis))
    self.axis_min.setText(Standa.get_edges(self.axis)[0])
    self.axis_max.setText(Standa.get_edges(self.axis)[1])

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

  def vertical_init(self):
    steps = int(self.v_steps.text())
    speed = int(self.v_speed.text())

    Standa.set_speed(self.vertical, speed)
    Standa.shift_on(self.vertical, steps, 0)
    Standa.shift_on(self.vertical, -steps, 0)
    self.v_position.setText(Standa.get_position(self.vertical))

  def vertical_shift_on(self):
    Standa.shift_on(self.vertical, int(self.v_steps.text()), 0)
    self.v_position.setText(Standa.get_position(self.vertical))

  def vertical_move_to(self):
    Standa.move_to(self.vertical, int(self.v_there.text()), 0)
    self.v_position.setText(Standa.get_position(self.vertical))

  def vertical_home(self):
    Standa.go_home(self.vertical)
    self.v_position.setText(Standa.get_position(self.vertical))

  def axis_init(self):
    self.axis = Standa.device(self.axis_address.text())

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


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
