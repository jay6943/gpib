import time
import libximc.highlevel as ximc

# Virtual device will be used by default.
# In case you have real hardware set correct device URI here

device_uri = r'xi-com:\\.\COM5'                              # Serial port
# device_uri = r'xi-emu:///ABS_PATH/virtual_controller.bin'  # Virtual device
# device_uri = 'xi-tcp://172.16.130.155:1820'                # Raw TCP connection
# device_uri = 'xi-net://192.168.1.120/abcd'                 # XiNet connection

axis = ximc.Axis(device_uri)
axis.open_device()

print('Launch movement...')
axis.command_right()

time.sleep(3)

print('Stop movement')
axis.command_stop()

# It's also called automatically by garbage collector, so explicit closing is optional
print('Disconnect device')
axis.close_device()

print('Done')
