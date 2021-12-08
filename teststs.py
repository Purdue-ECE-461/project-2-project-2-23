from TrustworthyModules.Main import run_rank_mode
import sys


if __name__ == '__main__':
    base64_encoded, dict = run_rank_mode(sys.argv[1])
    print(dict)