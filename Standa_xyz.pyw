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
    self.setGeometry(500, 500, 680, 300)

    self.laxis = Standa.linear()
    self.vaxis = Standa.vertical()

    dat.Qbutton(self, self.linear_move, 'Linear', 0, 0, 120)
    self.l_steps = dat.Qedit(self, '100', 130, 0, 120)
    self.l_position = dat.Qedit(self, '', 260, 0, 120)
    self.l_speed = dat.Qedit(self, '500', 520, 0, 120)

    dat.Qbutton(self, self.vertical_move, 'Vertical', 0, 80, 120)
    self.v_steps = dat.Qedit(self, '100', 130, 80, 120)
    self.v_position = dat.Qedit(self, '', 260, 80, 120)
    self.v_speed = dat.Qedit(self, '100', 520, 80, 120)
    dat.Qbutton(self, self.vertical_home, 'Home', 0, 120, 120)

    self.l_position.setText(self.laxis.get_position())
    self.v_position.setText(self.vaxis.get_position())

  def linear_move(self):
    steps = int(self.l_steps.text())
    speed = int(self.l_speed.text())

    self.laxis.move_speed(steps, 0, speed)
    self.l_position.setText(self.laxis.get_position())

  def vertical_move(self):
    steps = int(self.v_steps.text())
    speed = int(self.v_speed.text())

    self.vaxis.move_speed(steps, 0, speed)
    self.v_position.setText(self.vaxis.get_position())

  def vertical_home(self):
    self.vaxis.go_home()

    self.v_position.setText(self.vaxis.get_position())


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = motors()
  window.show()
  sys.exit(app.exec_())
