import dev

ldc = dev.E_Tek_DLDC_1002()

ldc.write('RES')
ldc.write('SCH1')
ldc.write('STP23')
# ldc.write('SLD10')

ldc.close()
