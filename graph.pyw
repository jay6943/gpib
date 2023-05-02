import os
import sys
import dat
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class App(Qw.QWidget):

  def __init__(self):

    super().__init__()

    self.i = 0

    self.x = []
    self.y = []

    self.legend = []

    self.xmin, self.xmax = 0, 0
    self.ymin, self.ymax = 0, 0

    self.setWindowTitle('Graph')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 100, 540, 350)

    dat.Qbutton(self, self.onOpen, 'Open', 0, 0, 100)
    dat.Qbutton(self, self.onOpenFiles, 'Multiple files', 100, 0, 100)
    dat.Qbutton(self, self.onDraw, 'Draw', 200, 0, 100)
    dat.Qbutton(self, self.onClear, 'Clear', 300, 0, 100)
    dat.Qbutton(self, self.onSave, 'Save', 400, 0, 100)

    dat.Qlabel(self, 'Min', 150, 160, 40)
    dat.Qlabel(self, 'Max', 290, 160, 40)
    dat.Qlabel(self, 'Step', 430, 160, 40)
    dat.Qlabel(self, 'X axis', 10, 185, 60)
    dat.Qlabel(self, 'Y axis', 10, 225, 60)
    dat.Qlabel(self, 'Line style', 10, 265, 60)

    self.title = dat.Qedit(self, 'filename', 0, 40, 500)
    self.xmins = dat.Qedit(self, '', 100, 200, 120)
    self.xmaxs = dat.Qedit(self, '', 240, 200, 120)
    self.xmids = dat.Qedit(self, '', 380, 200, 120)
    self.ymins = dat.Qedit(self, '', 100, 240, 120)
    self.ymaxs = dat.Qedit(self, '', 240, 240, 120)
    self.ymids = dat.Qedit(self, '', 380, 240, 120)
    self.marks = dat.Qedit(self, '-',100, 280, 120)
    self.xlabel = dat.Qedit(self, 'X', 0, 80, 240)
    self.ylabel = dat.Qedit(self, 'Y', 260, 80, 240)

    self.checkTitle = dat.Qcheck(self, 'Title', 240, 280, 100)
    self.checkLegend = dat.Qcheck(self, 'Legend', 300, 280, 100)

    self.checkTitle.setChecked(False)
    self.checkLegend.setChecked(True)

  def onXtitle(self, text):
    self.xlabel.setText(text)

  def onYtitle(self, text):
    self.ylabel.setText(text)

  def OnFolder(self):
    folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.get_folder())

    if folder != '': dat.set_folder(folder)

  def onSearch(self):
    for i in range(len(self.x)):

      xmin, xmax = min(self.x[i]), max(self.x[i])
      ymin, ymax = min(self.y[i]), max(self.y[i])

      if i < 1:
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax
      else:
        if xmin < self.xmin: self.xmin = xmin
        if xmax > self.xmax: self.xmax = xmax
        if ymin < self.ymin: self.ymin = ymin
        if ymax > self.ymax: self.ymax = ymax

    self.xmins.setText(str(round(self.xmin, 6)))
    self.xmaxs.setText(str(round(self.xmax, 6)))
    self.ymins.setText(str(round(self.ymin, 6)))
    self.ymaxs.setText(str(round(self.ymax, 6)))

  def onOpen(self):
    fileName = Qw.QFileDialog.getOpenFileName(self, '', dat.get_folder(), '*.txt;;*.dat')[0]
    print(fileName)
    folder = os.path.dirname(fileName)
    print(folder)

    if fileName:
      dat.set_folder(folder)

      self.x.append([])
      self.y.append([])

      data = np.loadtxt(fileName).transpose()
      self.x[self.i], self.y[self.i] = data[0], data[1]

      self.onSearch()

      title = fileName[:-4].split('/')
      self.title.setText(title[-1])
      self.legend.append(title[-1])

      self.i += 1

  def onOpenFiles(self):
    files = Qw.QFileDialog.getOpenFileNames(self, '', dat.get_folder(), '*.txt;;*.dat')[0]

    for i in range(len(files)):
      folder = os.path.dirname(files[i])

      self.x.append([])
      self.y.append([])

      data = np.loadtxt(files[i]).transpose()
      self.x[i], self.y[i] = data[0], data[1]

      title = files[i][:-4].split('/')
      self.legend.append(title[-1])

    if len(files) > 0: self.onSearch()

    self.i += len(files)

  def onPlot(self, fileName):
    for i in range(self.i): plt.plot(self.x[i], self.y[i], self.marks.text())
    plt.xlabel(self.xlabel.text())
    plt.ylabel(self.ylabel.text())
    if self.checkTitle.isChecked(): plt.title(self.title.text())
    if self.checkLegend.isChecked(): plt.legend(self.legend)
    plt.grid()
    if len(fileName) > 0: plt.savefig(fileName)
    else: plt.show()

  def onSave(self):
    text = dat.get_folder() + '/' + self.title.text()
    fileName = Qw.QFileDialog.getSaveFileName(self, '', text, '*.png')[0]
    if self.i > 0 and fileName: self.onPlot(fileName)

  def onDraw(self):
    if self.i > 0: self.onPlot('')

  def onClear(self):
    self.i = 0

    del self.x
    del self.y

    self.legend = []

    self.title.setText('')
    self.xmins.setText('')
    self.xmaxs.setText('')
    self.ymins.setText('')
    self.ymaxs.setText('')

    self.x = []
    self.y = []

if __name__ ==  '__main__':

  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())
