import sys
import dev
import dat
import keyboard
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


class Power_Monitoring(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.setWindowTitle('PD')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(200, 200, 200, 130)

    dat.Qbutton(self, self.start, 'Start', 0, 0, 160)
    self.m = dat.Qedit(self, '0.3', 0, 60, 160)

  def start(self):
    pd = dev.Keysight_81630B_photodiode()

    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 8))
    y = []
    while True:
      if keyboard.is_pressed('esc'):
        break

      y.append(pd.fetch(1, 1))

      ax.clear()
      ax.plot(y)
      ax.grid()

      plt.show()
      plt.pause(float(self.m.text()))

    plt.close()
    pd.close()


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Power_Monitoring()
  window.show()
  sys.exit(app.exec_())
