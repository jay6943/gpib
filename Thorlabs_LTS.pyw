import sys
import dat
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import thorlabs_apt as apt

class App(Qw.QWidget):

  def __init__(self):
    super().__init__()
    
    y, dy = 80, 50

    self.setWindowTitle('LTS')
    self.setWindowIcon(Qg.QIcon('thorlabs.png'))
    self.setGeometry(100, 50, 210, y+350)

    dat.Qbutton(self, self.OnConn, 'Connect', 90, y-80, dy + 30)
    dat.Qbutton(self, self.OnMove, 'MOVE', 0, y, dy)
    dat.Qbutton(self, self.OnHome, 'HOME', 120, y, dy)
    dat.Qbutton(self, self.On1p, '+', 0, y+40, dy)
    dat.Qbutton(self, self.On1n, '-', 60, y+40, dy)
    dat.Qbutton(self, self.On2p, '+', 0, y+80, dy)
    dat.Qbutton(self, self.On2n, '-', 60, y+80, dy)
    dat.Qbutton(self, self.On3p, '+', 0, y+120, dy)
    dat.Qbutton(self, self.On3n, '-', 60, y+120, dy)
    dat.Qbutton(self, self.On4p, '+', 0, y+160, dy)
    dat.Qbutton(self, self.On4n, '-', 60, y+160, dy)
    dat.Qbutton(self, self.On5p, '+', 0, y+200, dy)
    dat.Qbutton(self, self.On5n, '-', 60, y+200, dy)
    dat.Qbutton(self, self.On6p, '+', 0, y+240, dy)
    dat.Qbutton(self, self.On6n, '-', 60, y+240, dy)
    dat.Qbutton(self, self.On7p, '+', 0, y+280, dy)
    dat.Qbutton(self, self.On7n, '-', 60, y+280, dy)

    # 45151484, 45288094
    self.con = dat.Qedit(self, '45288094', 0, y-80, 80)
    self.prt = dat.Qedit(self, 'LTS150', 0, y-40, 170)
    self.txt = dat.Qedit(self, '10', 60, y, dy)
    self.On1 = dat.Qedit(self, '0.01', 120, y+40, dy)
    self.On2 = dat.Qedit(self, '0.05', 120, y+80, dy)
    self.On3 = dat.Qedit(self, '0.25', 120, y+120, dy)
    self.On4 = dat.Qedit(self, '0.5', 120, y+160, dy)
    self.On5 = dat.Qedit(self, '1.4', 120, y+200, dy)
    self.On6 = dat.Qedit(self, '10.4', 120, y+240, dy)
    self.On7 = dat.Qedit(self, '20', 120, y+280, dy)

  def OnConn(self):
    self.prt.setText('')
    self.stage = apt.Motor(45288094)
    self.prt.setText('LTS150')

  def OnStep(self, text, sign):
    self.x = self.x + sign * float(text)
    self.stage.move_to(round(self.x, 3))

  def OnMove(self):
    self.OnStep(self.txt.text(), 1)

  def OnHome(self):
    self.stage.move_home(True)

  def On1p(self):
    self.OnStep(self.On1.text(), 1)

  def On1n(self):
    self.OnStep(self.On1.text(), -1)

  def On2p(self):
    self.OnStep(self.On2.text(), 1)

  def On2n(self):
    self.OnStep(self.On2.text(), -1)

  def On3p(self):
    self.OnStep(self.On3.text(), 1)

  def On3n(self):
    self.OnStep(self.On3.text(), -1)

  def On4p(self):
    self.OnStep(self.On4.text(), 1)

  def On4n(self):
    self.OnStep(self.On4.text(), -1)

  def On5p(self):
    self.OnStep(self.On5.text(), 1)

  def On5n(self):
    self.OnStep(self.On5.text(), -1)

  def On6p(self):
    self.OnStep(self.On6.text(), 1)

  def On6n(self):
    self.OnStep(self.On6.text(), -1)

  def On7p(self):
    self.OnStep(self.On7.text(), 1)

  def On7n(self):
    self.OnStep(self.On7.text(), -1)

if __name__ ==  '__main__':
  
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())
