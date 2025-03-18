import sys
import dev
import dat
import keyboard
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


class Power_Monitoring(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.setWindowTitle('PD monitor')
    self.setWindowIcon(Qg.QIcon('../doc/jk.png'))
    self.setGeometry(800, 200, 300, 160)

    dat.QbuttonBig(self, self.start, 'Power Monitoring', 0, 0, 260)
    self.m = dat.Qeditbig(self, '0.2', 0, 70, 260)

  def start(self):
    pd = dev.Keysight_81630B_photodiode()

    y = np.ones(101) * pd.fetch(1, 1)

    plt.ion()
    plt.figure(figsize=(10, 6))

    while True:
      if keyboard.is_pressed('esc'):
        break

      y = np.roll(y, -1)
      y[-1] = pd.fetch(1, 1)

      plt.cla()
      plt.plot(y)
      plt.xlabel('Numbers')
      plt.ylabel('Output power (dBm)')
      plt.xlim(0, 100)
      plt.grid()
      plt.show()
      plt.pause(float(self.m.text()))

    plt.close()
    pd.close()


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Power_Monitoring()
  window.show()
  sys.exit(app.exec_())
