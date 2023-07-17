import os
import sys
import dat
import dev
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

def OnMax():
  dev.osa(':CALC:MARK:MAX')

def OnMin():
  dev.osa(':CALC:MARK:MIN')

def OnMarkCenter():
  dev.osa(':CALC:MARK:SCEN')

def OnContinuous():
  osa = dev.osa(False)
  osa.write(':INIT:SMOD REP')
  osa.write(':INIT:IMM')
  osa.close()

def OnSingle():
  osa = dev.osa(False)
  osa.write(':INIT:SMOD SING')
  osa.write(':INIT:IMM')
  osa.close()

class ExWindow(Qw.QMainWindow):
  
  def __init__(self):

    super().__init__()

    self.y = None
    self.x = None

    self.setWindowTitle('OSA')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(500, 500, 290, 450)

    osa = dev.osa(False)
    center = float(osa.query(':SENS:WAV:CENT?')) * 1e9
    span = float(osa.query(':SENS:WAV:SPAN?')) * 1e9
    res = float(osa.query(':SENS:BAND:RES?')) * 1e9
    rlev = float(osa.query(':DISP:TRAC:Y1:RLEV?'))
    pdiv = float(osa.query(':DISP:TRAC:Y1:PDIV?'))
    osa.close()

    self.center = dat.Qedit(self, str(center), 0, 60, 120)
    self.span = dat.Qedit(self, str(span), 0, 100, 120)
    self.bandwidth = dat.Qedit(self, str(res), 0, 140, 120)
    self.sensitivity = dat.Qedit(self, '10', 0, 180, 120)
    self.reference = dat.Qedit(self, str(rlev), 0, 220, 120)
    self.division = dat.Qedit(self, str(pdiv), 0, 260, 120)

    dat.Qbutton(self, self.OnCenter, 'Center (nm)', 130, 60, 120)
    dat.Qbutton(self, self.OnSpan, 'Span (nm)', 130, 100, 120)
    dat.Qbutton(self, self.OnBandwidth, 'Bandwidth (nm)', 130, 140, 120)
    dat.Qbutton(self, self.OnSensitivity, 'Sensitivity (dBm)', 130, 180, 120)
    dat.Qbutton(self, self.OnReference, 'Reference (dBm)', 130, 220, 120)
    dat.Qbutton(self, self.OnDivision, 'Division (dB)', 130, 260, 120)

    dat.Qbutton(self, self.OnGet, 'Get', 0, 0, 120)
    dat.Qbutton(self, self.OnSave, 'Save', 130, 0, 120)
    dat.Qbutton(self, OnContinuous, 'Continuous', 0, 300, 120)
    dat.Qbutton(self, OnSingle, 'Stop', 130, 300, 120)

    dat.Qbutton(self, OnMax, 'Max', 0, 340, 120)
    dat.Qbutton(self, OnMin, 'Min', 130, 340, 120)
    dat.Qbutton(self, OnMarkCenter, 'Mark to Center', 0, 380, 120)
    dat.Qbutton(self, self.OnLevel, 'Ref. to Peak', 130, 380, 120)
    
    self.saving = dat.Qcheck(self, 'Save w/o show', 10, 30, 120)
    self.figure = dat.Qcheck(self, 'Save figure', 150, 30, 120)

    self.setSwitch = 1
    self.figure.setChecked(True)

  def OnPoints(self):

    c = float(self.span.text())
    d = float(self.bandwidth.text())
    m = int(round(c / d, 0)) * 10 + 1

    dev.osa(':SENS:SWE:POIN ' + str(m))

  def OnCenter(self):
    dev.osa(':SENS:WAV:CENT ' + self.center.text() + 'NM')

  def OnSpan(self):
    dev.osa(':SENS:WAV:SPAN ' + self.span.text() + 'NM')

  def OnBandwidth(self):
    dev.osa(':SENS:BAND:RES ' + self.bandwidth.text() + 'NM')

  def OnSensitivity(self):
    dev.osa(':DISP:TRAC:Y1:RPOS ' + self.sensitivity.text() + 'DIV')

  def OnReference(self):
    dev.osa(':DISP:TRAC:Y1:RLEV ' + self.reference.text() + 'DBM')

  def OnDivision(self):
    dev.osa(':DISP:TRAC:Y1:PDIV ' + self.division.text() + 'DB')

  def OnLevel(self):
    osa = dev.osa(False)
    osa.write(':CALC:MARK:MAX')
    y = float(osa.query(':CALC:MARK:Y?'))
    osa.close()
    
    self.reference.setText(str(round(y, 0)))
    self.OnReference()

  def OnGet(self):
    osa = dev.osa(False)
    osa.timeout = 50000
    OnSingle()
    self.x = osa.query(':TRAC:DATA:X? TRA')
    self.y = osa.query(':TRAC:DATA:Y? TRA')
    OnContinuous()
    osa.close()

    self.x = self.x.replace('\n', '').split(',')
    self.y = self.y.replace('\n', '').split(',')
    self.x = np.array(self.x).astype(float) * 1e9
    self.y = np.array(self.y).astype(float)
    self.x = np.round(self.x, 9)
    self.y = np.round(self.y, 9)

    xc = float(self.center.text())
    dx = float(self.span.text())
    yr = float(self.reference.text())
    dy = float(self.division.text())

    plt.close()
    plt.figure(dpi=150)
    plt.plot(self.x, self.y)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Output (dBm)')
    plt.xlim(xc - dx * 0.5, xc + dx * 0.5)
    plt.ylim(yr - dy * 10, yr)
    plt.grid()
    plt.show()

    if self.saving.isChecked(): self.OnSave()

  def OnSave(self):
    filename = Qw.QFileDialog.getSaveFileName(self, '', dat.get_folder(), '*.txt')[0]
    folder = os.path.dirname(filename)

    if filename:
      data = np.array([self.x, self.y])
      np.savetxt(filename, data.transpose(), fmt='%.3f')
      dat.set_folder(folder)
      if self.figure.isChecked():
        fp = os.path.splitext(filename)
        print(fp[0])
        plt.savefig(fp[0] + '.png')

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  ex = ExWindow()
  ex.show()
  sys.exit(app.exec_())