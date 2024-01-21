import sys
import pandas as pd

# sys.aargv are command line argumnets passed to the script
print(sys.argv)

# 0 is the name of the file, 1 is whatever is passed from command line
print(sys.argv[0])

day = sys.argv[1]

print(f'job complete on {day}, good job!')
