import os

path = '../data/SiN'

circ = r'$^{\circ}$'

def mkdir(folder):
  folder = f'{path}/{folder}'
  if not os.path.isdir(folder): os.mkdir(folder)

  return folder


def get_folder():
  fp = open('../data/cfg.txt')
  data = fp.read()
  data = data.replace('\n', '')
  fp.close()

  return data


def set_folder(folder):
  fp = open('../data/cfg.txt', 'w')
  fp.write(folder)
  fp.close()


if __name__ == '__main__':
  mkdir('EI-ICR-WG-R1-TV23-004/voa/t1/')
