import os
import sys
import dat
import dev
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

class App(Qw.QWidget):

  def __init__(self):

    super().__init__()
    
    self.setWindowTitle('ANDO')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 600, 280, 110)

    dat.Qbutton(self, self.OnGet, 'Get', 0, 0, 100)
    dat.Qbutton(self, self.OnSave, 'Save', 0, 40, 100)

    self.A = dat.Qedit(self, '', 110, 0, 100)
    self.B = dat.Qedit(self, '', 110, 40, 100)

    self.checkA = dat.Qcheck(self, 'A', 220, 0, 100)
    self.checkB = dat.Qcheck(self, 'B', 220, 40, 100)

    self.checkA.setChecked(True)
    self.checkB.setChecked(False)

    opm = dev.ando()
    opm.write('AA')
    opm.close()

    self.getData = 0

  def OnGet(self):
    opm = dev.ando()
    self.Ap, self.Bp = opm.query()
    self.A.setText(str(self.Ap))
    self.B.setText(str(self.Bp))
    opm.close()

    self.getData = 1

  def OnSave(self):

    fp = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

    data = []

    if self.getData and fp:
      if self.checkA.isChecked(): data = data + [self.Ap]
      if self.checkB.isChecked(): data = data + [self.Bp]

      np.savetxt(fp, np.array(data), fmt='%.3f')

      folder = os.path.dirname(fp)
      if folder != dat.getfolder(): dat.setfolder(folder)

if __name__ ==  '__main__':
  
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())
