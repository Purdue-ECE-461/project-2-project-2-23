from TrustworthyModules.Main import run_rank_mode
import sys
from TrustworthyModules.RunTests import runtests


if __name__ == '__main__':
    #runtests()
    _,_ = run_rank_mode(sys.argv[1])