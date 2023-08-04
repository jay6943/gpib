import sys
import dat
import dev
import time
import os
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

import pyvisa as visa
VISA_ADDRESS = 'GPIB1::17::INSTR'
# Create a connection (session) to the instrument
resourceManager = visa.ResourceManager()
TLD = resourceManager.open_resource(VISA_ADDRESS)
print(TLD.query('*IDN?'))
timesleep = 1.5 # 중간 time sleep 시간
cwd = os.getcwd()

class App(Qw.QWidget):

    def __init__(self):

        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):

        self.setWindowTitle('8163B') #Bar name
        self.setWindowIcon(Qg.QIcon('ni.png')) # Bar name 그림
        self.setGeometry(0, 0, 520, 200) # top left: x,y bottom right x,y

        dat.Qbutton(self, self.OnPower, 'Power (dBm)', 0, 0, 100) #self.OnPower: button id, button name,  button top left x,y, button 길이
        dat.Qbutton(self, self.OnWavelength, 'Wavelength (nm) No grid', 0, 40, 150) #self.OnWavelength: button id
        dat.Qbutton(self, self.OnSweep, 'Sweep from to step(nm)', 0, 90, 150) 
        
        self.power = dat.Qedit(self, '10', 160, 0, 100) #Edit창 
        self.wavelength = dat.Qedit(self, '1550', 160, 40, 100)

        dat.Qlabel(self, 'From nm', 160, 65)
        dat.Qlabel(self, 'To nm', 270, 65)
        dat.Qlabel(self, 'Step nm', 380, 65)

        
        self.SweepFrom = dat.Qedit(self, '1535', 160, 90, 100)
        self.SweepTo = dat.Qedit(self, '1565', 270, 90, 100)
        self.SweepStep = dat.Qedit(self, '0.1', 380, 90, 100)

        dat.Qbutton(self, self.On, 'ON', 270, 0, 100)
        dat.Qbutton(self, self.Off, 'OFF', 380, 0, 100)

        dat.Qbutton(self, self.OnSave, 'Save (auto)', 0,140, 100)
        dat.Qbutton(self, self.OnFolder, 'Set Folder', 270, 140, 100)
        self.filename = dat.Qedit(self, 'File name', 110, 140, 140)
        self.folder = dat.Qedit(self, cwd, 380, 140, 100)

        

    def OnPower(self): #위에서 설정한 Power 버튼 activation
        #  tld = dev.N7711A()
        TLD
        resourceManager = visa.ResourceManager()
        TLD = resourceManager.open_resource(VISA_ADDRESS)
        print(TLD.query('*IDN?'))
        TLD.query('sour1:pow ' + self.power.text() + 'dBm')
        TLD.close()
        
    def OnWavelength(self):
        # tld = dev.8163B()
        #TLD = resourceManager.open_resource(VISA_ADDRESS)
        TLD.query('sour1:wav ' + self.wavelength.text() + 'nm')
        #wav0 = tld.query('sour1:wav?')
        #print(str(wav0))
        #wav1 = tld.read_raw()
        #print(str(wav1))
  
        TLD.close()

    def On(self):
        # tld = dev.8163B()
        #TLD = resourceManager.open_resource(VISA_ADDRESS)
        print(TLD.query('*IDN?'))
        TLD.write('sour1:pow:stat 1')
        TLD.close() 

    def Off(self):
        #  tld = dev.8163B()
        #TLD = resourceManager.open_resource(VISA_ADDRESS)
        TLD.query('sour1:pow:stat 0')
        TLD.close()
  
    def OnSweep(self):

        From1 = float(self.SweepFrom.text())
        To1   = float(self.SweepTo.text())
        Step1 = float(self.SweepStep.text())
        Waveleng = np.arange(From1, To1+Step1, Step1)
                
        self.x = []
        self.y = []        

        #TLD = resourceManager.open_resource(VISA_ADDRESS)
        TLD.write('sour1:pow:stat 1')
        opm = dev.ando()
        for i in range(len(Waveleng)):
            time.sleep(timesleep)
            From1 = From1 + Step1
            TLD.write('sour1:wav ' + str(From1) + 'nm')
            
           
            a, b = opm.query()
            self.x.append(Waveleng[i])
            self.y.append(b)

            plt.cla()
            plt.plot(self.x, self.y)
            plt.grid()
            plt.xlabel('Wavelegnth (nm)')
            plt.ylabel('Optical Power (dBm)')
          #  plt.pause(timesleep)


        plt.show()
        TLD = resourceManager.open_resource(VISA_ADDRESS)
        TLD.write('sour1:pow:stat 0')
        
        TLD.close()
        opm.close()
        self.OnSave()

    def OnSave(self):
        print(dat.getfolder() + self.filename.text())
        print(self.x)
        print(self.y)
        print(str(self.x[1])+' '+str(self.y[1]))
        if self.filename.text():
            for i in range(len(self.x)):                
                f = open(dat.getfolder() + self.filename.text() +'.txt','a')
                f.write(str(self.x[i])+' '+str(self.y[i])+'\n')
                f.close()
                
 #           plt.cla()
 #           plt.plot(self.x, self.y)
 #           plt.xlabel('Wavelegnth (nm)')
 #           plt.ylabel('Optical Power (dBm)')
 #           plt.grid()
            plt.savefig(dat.getfolder() + self.filename.text() +'.png')
 

    def OnFolder(self):
        folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.getfolder())
        if folder != '':
            dat.setfolder(folder)
            self.folder.setText(dat.getfolder()) 
       




if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())
