import dev


def test():
    mbl = dev.Maiman_Laser_TEC()
    # mbl.write('dur:value 1')
    # mbl.write('freq:value 0')
    print(mbl.read('tec:temp:real?'))
    print(mbl.read('curr:real?'))
    mbl.close()

if __name__ == '__main__':
  test()
