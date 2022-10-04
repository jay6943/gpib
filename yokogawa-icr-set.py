import dev

osa = dev.osa(False)
osa.write(':SENS:WAV:CENT 1550NM')
osa.write(':SENS:WAV:SPAN 2NM')
osa.write(':SENS:BAND:RES 0.01NM')
osa.write(':DISP:TRAC:Y1:RLEV 0DBM')
osa.write(':DISP:TRAC:Y1:PDIV 10DB')
osa.write(':INIT:SMOD REP')
osa.write(':INIT:IMM')
osa.close()