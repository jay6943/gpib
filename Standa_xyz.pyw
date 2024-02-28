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

    self.laxis = Standa.linear()
    self.vaxis = Standa.vertical()

    dat.Qbutton(self, self.linear_move, 'Linear', 0, 0, 120)
    dat.Qbutton(self, self.linear_position, 'Position', 130, 0, 120)
    dat.Qbutton(self, self.linear_test, 'Test', 260, 0, 120)
    self.l_steps = dat.Qedit(self, '100', 0, 40, 120)
    self.l_position = dat.Qedit(self, '', 130, 40, 120)
    self.l_speed = dat.Qedit(self, '', 260, 40, 120)
    dat.Qlabel(self, self.laxis.get_edges(), 10, 70, 200)

    dat.Qbutton(self, self.vertical_move, 'Vertical', 0, 120, 120)
    dat.Qbutton(self, self.vertical_position, 'Position', 130, 120, 120)
    dat.Qbutton(self, self.vertical_test, 'Test', 260, 120, 120)
    self.v_steps = dat.Qedit(self, '50', 0, 160, 120)
    self.v_position = dat.Qedit(self, '', 130, 160, 120)
    self.v_speed = dat.Qedit(self, '', 260, 160, 120)
    dat.Qlabel(self, self.vaxis.get_edges(), 10, 190, 200)
    dat.Qbutton(self, self.vertical_home, 'Home', 260, 200, 120)

    self.l_position.setText(self.laxis.get_position())
    self.v_position.setText(self.vaxis.get_position())
    self.l_speed.setText(self.laxis.get_speed())
    self.v_speed.setText(self.vaxis.get_speed())

  def linear_move(self):
    steps = int(self.l_steps.text())
    speed = int(self.l_speed.text())

    self.laxis.move_speed(steps, 0, speed)
    self.l_position.setText(self.laxis.get_position())

  def linear_position(self):
    steps = int(self.l_steps.text())

    self.laxis.move(steps, 0)
    self.l_position.setText(self.laxis.get_position())

  def linear_test(self):
    steps = int(self.l_steps.text())

    self.laxis.move(steps, 0)
    self.laxis.move(-steps, 0)
    self.l_position.setText(self.laxis.get_position())

  def vertical_move(self):
    steps = int(self.v_steps.text())
    speed = int(self.v_speed.text())

    self.vaxis.move_speed(steps, 0, speed)
    self.v_position.setText(self.vaxis.get_position())

  def vertical_position(self):
    steps = int(self.v_steps.text())

    self.vaxis.move(steps, 0)
    self.v_position.setText(self.vaxis.get_position())

  def vertical_test(self):
    steps = int(self.v_steps.text())

    self.vaxis.move(steps, 0)
    self.vaxis.move(-steps, 0)
    self.v_position.setText(self.vaxis.get_position())

  def vertical_home(self):
    self.vaxis.go_home()
    self.v_position.setText(self.vaxis.get_position())


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
