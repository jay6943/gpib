import os

cdir = os.getcwd().split('\\')
root = ''

for cd in cdir[:-1]: root += cd + '/'

works = root[0] + root[1] + '/data/SiN/'
temps = root + 'data/cfg.txt'

def mkdir(folder):
  folders = folder.split('/')
  folder = works
  for fp in folders[:-1]:
    folder += fp + '/'
    if not os.path.isdir(folder): os.mkdir(folder)

  return folder


def get_folder():
  fp = open(temps)
  data = fp.read()
  data = data.replace('\n', '')
  fp.close()

  return data


def set_folder(folder):
  fp = open(temps, 'w')
  fp.write(folder)
  fp.close()

def get_gpib():
  fp = open(root + 'data/gpib.txt')
  gpib = fp.read()
  fp.close()

  return gpib


if __name__ == '__main__':
  # mkdir('EI-ICR-WG-R1-TV23-004/voa/t1/')
  print(get_gpib())
