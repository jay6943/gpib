import os
import sys
import dat
import dev
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class ExWindow(Qw.QMainWindow):
  
  def __init__(self):

    super().__init__()

    self.setWindowTitle('OSA')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 500, 290, 450)

    self.center = dat.Qedit(self, '1550', 0, 60, 120)
    self.span = dat.Qedit(self, '80', 0, 100, 120)
    # self.start = dat.Qedit(self, '1530', 0, 60, 120)
    # self.stop = dat.Qedit(self, '1570', 0, 100, 120)
    self.bandwidth = dat.Qedit(self, '1', 0, 140, 120)
    self.sensitivity = dat.Qedit(self, '10', 0, 180, 120)
    self.reference = dat.Qedit(self, '0', 0, 220, 120)
    self.division = dat.Qedit(self, '10', 0, 260, 120)

    dat.Qbutton(self, self.OnCenter, 'Center (nm)', 130, 60, 120)
    dat.Qbutton(self, self.OnSpan, 'Span (nm)', 130, 100, 120)
    # dat.Qbutton(self, self.OnStart, 'Start (nm)', 130, 60, 120)
    # dat.Qbutton(self, self.OnStop, 'Stop (nm)', 130, 100, 120)
    dat.Qbutton(self, self.OnBandwidth, 'Bandwidth (nm)', 130, 140, 120)
    dat.Qbutton(self, self.OnSensitivity, 'Sensitivity (dBm)', 130, 180, 120)
    dat.Qbutton(self, self.OnReference, 'Reference (dBm)', 130, 220, 120)
    dat.Qbutton(self, self.OnDivision, 'Division (dB)', 130, 260, 120)

    dat.Qbutton(self, self.OnGet, 'Get', 0, 0, 120)
    dat.Qbutton(self, self.OnSave, 'Save', 130, 0, 120)
    dat.Qbutton(self, self.OnContinuous, 'Continuous', 0, 300, 120)
    dat.Qbutton(self, self.OnSingle, 'Stop', 130, 300, 120)

    dat.Qbutton(self, self.OnMax, 'Max', 0, 340, 120)
    dat.Qbutton(self, self.OnMin, 'Min', 130, 340, 120)
    dat.Qbutton(self, self.OnMarkCenter, 'Mark to Center', 0, 380, 120)
    dat.Qbutton(self, self.OnLevel, 'Ref. to Peak', 130, 380, 120)
    
    self.saving = dat.Qcheck(self, 'Save w/o show', 10, 30, 120)
    self.figure = dat.Qcheck(self, 'Save figure', 150, 30, 120)

    osa = dev.osa(False)
    osa.write(':SENS:WAV:CENT ' + self.center.text() + 'NM')
    osa.write(':SENS:WAV:SPAN ' + self.span.text() + 'NM')
    # osa.write(':SENS:WAV:STAR ' + self.start.text() + 'NM')
    # osa.write(':SENS:WAV:STOP ' + self.stop.text() + 'NM')
    osa.write(':SENS:BAND:RES ' + self.bandwidth.text() + 'NM')
    osa.write(':DISP:TRAC:Y1:RLEV ' + self.reference.text() + 'DBM')
    osa.write(':DISP:TRAC:Y1:PDIV ' + self.division.text() + 'DB')
    # osa.write(':SENS:SWE:POIN ' + str(self.OnPoints()))
    osa.write(':INIT:SMOD REP')
    osa.write(':INIT:IMM')
    osa.close()

    self.setSwitch = 1
    self.figure.setChecked(True)

  def OnPoints(self):

    # a = float(self.start.text())
    # b = float(self.stop.text())
    # c = b - a

    c = float(self.span.text())
    d = float(self.bandwidth.text())
    m = int(round(c / d, 0)) * 10 + 1

    dev.osa(':SENS:SWE:POIN ' + str(m))

  def OnCenter(self):
    dev.osa(':SENS:WAV:CENT ' + self.center.text() + 'NM')

  def OnSpan(self):
    dev.osa(':SENS:WAV:SPAN ' + self.span.text() + 'NM')

  # def OnStart(self):
  #   dev.osa(':SENS:WAV:STAR ' + self.start.text() + 'NM')

  # def OnStop(self):
  #   dev.osa(':SENS:WAV:STOP ' + self.stop.text() + 'NM')

  def OnBandwidth(self):
    dev.osa(':SENS:BAND:RES ' + self.bandwidth.text() + 'NM')
    # self.OnPoints()

  def OnSensitivity(self):
    dev.osa(':DISP:TRAC:Y1:RPOS ' + self.sensitivity.text() + 'DIV')

  def OnReference(self):
    dev.osa(':DISP:TRAC:Y1:RLEV ' + self.reference.text() + 'DBM')

  def OnDivision(self):
    dev.osa(':DISP:TRAC:Y1:PDIV ' + self.division.text() + 'DB')

  def OnMax(self):
    dev.osa(':CALC:MARK:MAX')

  def OnMin(self):
    dev.osa(':CALC:MARK:MIN')

  def OnLevel(self):
    osa = dev.osa(False)
    osa.write(':CALC:MARK:MAX')
    y = float(osa.query(':CALC:MARK:Y?'))
    osa.close()
    
    self.reference.setText(str(round(y, 0)))
    self.OnReference()

  def OnMarkCenter(self):
    dev.osa(':CALC:MARK:SCEN')
      
  def OnContinuous(self):
    osa = dev.osa(False)
    osa.write(':INIT:SMOD REP')
    osa.write(':INIT:IMM')
    osa.close()
  
  def OnSingle(self):
    osa = dev.osa(False)
    osa.write(':INIT:SMOD SING')
    osa.write(':INIT:IMM')
    osa.close()

  def OnGet(self):
    
    osa = dev.osa(False)
    osa.timeout = 50000
    self.OnSingle()
    self.x = osa.query(':TRAC:DATA:X? TRA')
    self.y = osa.query(':TRAC:DATA:Y? TRA')
    self.OnContinuous()
    osa.close()

    self.x = self.x.replace('\n', '').split(',')
    self.y = self.y.replace('\n', '').split(',')
    self.x = np.array(self.x).astype(float) * 1e9
    self.y = np.array(self.y).astype(float)
    self.x = np.round(self.x, 9)
    self.y = np.round(self.y, 9)

    xt = np.linspace(self.x[0], self.x[-1], 5)
    yt = np.linspace(-80, 0, 5)

    plt.close()
    plt.figure(dpi=150)
    plt.plot(self.x, self.y)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Output (dBm)')
    plt.xlim(xt[0], xt[-1])
    plt.ylim(yt[0], yt[-1])
    plt.xticks(xt)
    plt.yticks(yt)
    plt.grid()
    plt.show()

    if self.saving.isChecked(): self.OnSave()

  def OnSave(self):

    fp = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

    if fp:
      data = [self.x, self.y]
      np.savetxt(fp, np.array(data).transpose(), fmt='%.3f')
      if self.figure.isChecked(): plt.savefig(fp[:len(fp)-4] + '.png')

      folder = os.path.dirname(fp)
      if folder != dat.getfolder(): dat.setfolder(folder)

if __name__ == '__main__':

  app = Qw.QApplication(sys.argv)
  ex = ExWindow()
  ex.show()
  sys.exit(app.exec_())