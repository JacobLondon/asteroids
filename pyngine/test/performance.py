import cProfile
import sys
sys.path.append('..')

from src import *

c = Controller()
def debug():
    cProfile.run('c.run()')

if __name__ == '__main__':
    debug()
