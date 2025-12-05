import sys
import cfg
import dat
import dev
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw


class Ando_AQ_2105B(Qw.QWidget):
  def __init__(self):
    super().__init__()
    
    self.setWindowTitle('ANDO')
    self.setWindowIcon(Qg.QIcon('../doc/jk.png'))
    self.setGeometry(100, 600, 280, 110)

    dat.Qbutton(self, self.OnGet, 'Get', 0, 0, 100)
    dat.Qbutton(self, self.OnSave, 'Save', 0, 40, 100)

    self.A = dat.Qedit(self, '', 110, 0, 100)
    self.B = dat.Qedit(self, '', 110, 40, 100)

    self.checkA = dat.Qcheck(self, 'A', 220, 0, 100)
    self.checkB = dat.Qcheck(self, 'B', 220, 40, 100)

    self.checkA.setChecked(True)
    self.checkB.setChecked(False)

    opm = dev.Ando_AQ2105B_photodiode()
    opm.write('AA')
    opm.close()

    self.getData = 0

  def OnGet(self):
    opm = dev.Ando_AQ2105B_photodiode()
    Ap, Bp = opm.query()
    self.A.setText(str(Ap))
    self.B.setText(str(Bp))
    opm.close()

    self.getData = 1

  def OnSave(self):
    fp = Qw.QFileDialog.getSaveFileName(self, '', cfg.path, '*.txt')[0]
    data = []
    if self.getData and fp:
      if self.checkA.isChecked(): data += [self.Ap]
      if self.checkB.isChecked(): data += [self.Bp]
      np.savetxt(fp, np.array(data), fmt='%.3f')


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Ando_AQ_2105B()
  window.show()
  sys.exit(app.exec_())
