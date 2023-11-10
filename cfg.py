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

if __name__ == '__main__': mkdir('EI-ICR-WG-R1-TV23-004/voa/t1/')
