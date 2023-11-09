import dev

ldc = dev.Digital_Laser_Diode_Controller_1002()

ldc.write('RES')
ldc.write('SCH1')
ldc.write('STP23')
# ldc.write('SLD10')

ldc.close()
