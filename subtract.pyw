import sys
import dat
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class App(Qw.QWidget):

    def __init__(self):

        super().__init__()

        self.i = 0

        self.x = []
        self.y = []

        self.xr = []
        self.yr = []

        self.legend = []

        self.xtitles, self.ytitles = dat.titles()

        self.xmin, self.xmax = 0, 0
        self.ymin, self.ymax = 0, 0
        
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('Subtractor')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 540, 390)

        dat.Qbutton(self, self.onRefer, 'Reference', 0, 0, 80)
        dat.Qbutton(self, self.onOpen, 'Open', 80, 0, 80)
        dat.Qbutton(self, self.onOpenFiles, 'Multiple', 160, 0, 80)
        dat.Qbutton(self, self.onDraw, 'Draw', 240, 0, 80)
        dat.Qbutton(self, self.onClear, 'Clear', 320, 0, 80)
        dat.Qbutton(self, self.onSave, 'Save', 400, 0, 100)
        dat.Qbutton(self, self.onFolder, 'Set Folder', 380, 320, 120)

        dat.Qlabel(self, 'Min', 140, 200)
        dat.Qlabel(self, 'Max', 280, 200)
        dat.Qlabel(self, 'Step', 420, 200)
        dat.Qlabel(self, 'X axis', 0, 240)
        dat.Qlabel(self, 'Y axis', 0, 280)
        dat.Qlabel(self, 'Line style', 0, 320)

        self.refer = dat.Qedit(self, 'reference file', 0, 40, 500)
        self.title = dat.Qedit(self, 'target file', 0, 80, 500)
        self.xmins = dat.Qedit(self, '', 100, 240, 120)
        self.xmaxs = dat.Qedit(self, '', 240, 240, 120)
        self.xmids = dat.Qedit(self, '', 380, 240, 120)
        self.ymins = dat.Qedit(self, '', 100, 280, 120)
        self.ymaxs = dat.Qedit(self, '', 240, 280, 120)
        self.ymids = dat.Qedit(self, '', 380, 280, 120)
        self.marks = dat.Qedit(self, '-',100, 320, 120)

        self.xtitle(0, 120)
        self.ytitle(0, 160)

        self.checkTitle = dat.Qcheck(self, 'Title', 240, 320, 100)
        self.checkLegend = dat.Qcheck(self, 'Legend', 300, 320, 100)

        self.checkTitle.setChecked(False)
        self.checkLegend.setChecked(True)

    def xtitle(self, x, y):

        self.xlabel = dat.Qedit(self, 'X', x, y, 240)
        combo = dat.Qcombo(self, x + 240 + 20, y, 240)
        for title in self.xtitles: combo.addItem(title)
        combo.activated[str].connect(self.onXtitle)

    def ytitle(self, x, y):

        self.ylabel = dat.Qedit(self, 'Y', x, y, 240)
        combo = dat.Qcombo(self, x + 240 + 20, y, 240)
        for title in self.ytitles: combo.addItem(title)
        combo.activated[str].connect(self.onYtitle)
        
    def onXtitle(self, text):

        self.xlabel.setText(text)

    def onYtitle(self, text):

        self.ylabel.setText(text)

    def onFolder(self):

        folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.getfolder())

        if folder != '': dat.setfolder(folder)

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

    def onRefer(self):

        fileName = Qw.QFileDialog.getOpenFileName(self, '', dat.getfolder(), '*.txt;;*.dat')[0]
        
        if fileName:

            self.xr, self.yr = dat.getdata(fileName)

            title = fileName[:-4].split('/')
            self.refer.setText(title[-1])
                
    def onOpen(self):

        fileName = Qw.QFileDialog.getOpenFileName(self, '', dat.getfolder(), '*.txt;;*.dat')[0]
        
        if fileName:

            self.x.append([])
            self.y.append([])

            self.x[self.i], self.y[self.i] = dat.getdata(fileName)

            if len(self.yr) > 0:
                for j in range(len(self.y[self.i])):
                    self.y[self.i][j] = self.yr[j] - self.y[self.i][j]

            self.onSearch()

            title = fileName[:-4].split('/')
            self.title.setText(title[-1])
            self.legend.append(title[-1])

            self.i += 1

    def onOpenFiles(self):

        files = Qw.QFileDialog.getOpenFileNames(self, '', dat.getfolder(), '*.txt;;*.dat')[0]

        for i in range(len(files)):

            self.x.append([])
            self.y.append([])

            self.x[i], self.y[i] = dat.getdata(files[i])

            if len(self.yr) > 0:
                for j in range(len(self.y[i])):
                    self.y[i][j] = self.yr[j] - self.y[i][j]

            title = files[i][:-4].split('/')
            self.legend.append(title[-1])
        
        if len(files) > 0: self.onSearch()
        
        self.i += len(files)

    def onPlot(self, fileName):

        for i in range(self.i):
            plt.plot(self.x[i], self.y[i], self.marks.text())

        plt.xlabel(self.xlabel.text())
        plt.ylabel(self.ylabel.text())
        plt.xlim(float(self.xmins.text()), float(self.xmaxs.text()))
        plt.ylim(float(self.ymins.text()), float(self.ymaxs.text()))
        if self.checkTitle.isChecked(): plt.title(self.title.text())
        if self.checkLegend.isChecked(): plt.legend(self.legend)
        plt.grid()
        if len(fileName) > 0: plt.savefig(fileName)
        else: plt.show()
    
    def onSave(self):

        text = dat.getfolder() + '/' + self.title.text()

        fileName = Qw.QFileDialog.getSaveFileName(self, '', text, '*.png')[0]

        if self.i > 0 and fileName: self.onPlot(fileName)

    def onDraw(self):

        if self.i > 0: self.onPlot('')

    def onClear(self):

        self.i = 0

        self.x = []
        self.y = []

        self.legend = []

        self.title.setText('')
        self.xmins.setText('')
        self.xmaxs.setText('')
        self.ymins.setText('')
        self.ymaxs.setText('')

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())
