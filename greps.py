import re
import argparse
from colorama import Fore ,Style

# To use this code :
# We can directly type "python greps.py pattern file_name(1 or more with spaces) argument(1 or more with spaces)" in the terminal itself.
#For using spec enter "--spec no_of_line" along with context and other optional arguments.

parser = argparse.ArgumentParser(description='Search for patterns: ')
parser.add_argument('pattern', help='The pattern to search for')
parser.add_argument('files', nargs='+', help='List of files to search')
parser.add_argument('--search','-s',action='store_true', help='basic search')
parser.add_argument('-color', action='store_true', help='Colorize the matched pattern')
parser.add_argument('--count','-c', action='store_true', help='count lines')
parser.add_argument('--word', '-w',action='store_true', help='search whole word only')
parser.add_argument('--context','-C', action='store_true', help='context')
parser.add_argument('--spec', type=int, help='number of context lines to jump to')
parser.add_argument('--ignorecase', '-i',action='store_true', help='ignore case')
parser.add_argument('--invert','-v', action='store_true', help='invert search')

args = parser.parse_args()

if args.search:
    for file in args.files:
        with open(file) as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                match = re.search(args.pattern, line)
                if match:
                    line = re.sub(match.group(),f"{Fore.BLUE}{match.group()}{Style.RESET_ALL}", line)
                    print(f"{file}:{i}: {line}", end='')

if args.count:
    count=0
    for file in args.files:
        with open(file) as f:
                lines = f.readlines()
                for i, line in enumerate(lines, start=1):
                    match = re.search(args.pattern, line)
                    if match:
                        count += 1
    print(f'totol matching lines {count}')

if args.word:
    yo = args.pattern
    for file in args.files:
        with open(file) as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                match = re.search(f'\s{yo}\s', line)
                if match:
                    line = re.sub(match.group(), f"{Fore.RED}{match.group()}{Style.RESET_ALL}", line)
                    print(f"{file}:{i}: {line}", end='')
                    
if args.context:
    for file in args.files:
        with open(file) as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                match = re.search(args.pattern, line)
                if match:
                    line = re.sub(match.group(),f"{Fore.RED}{match.group()}{Style.RESET_ALL}", line)
                    print(f"{file}:{i}: {line}", end='')
                    if args.spec:
                        if i > args.spec:
                            print(f"{file}:{i-args.spec}: {lines[i-args.spec-1]}", end='')
                        if i < len(lines):
                            print(f"{file}:{i+args.spec}: {lines[i+args.spec-1]}", end='')
                    else:                        
                        if i > 1:
                            print(f"{file}:{i-1}: {lines[i-2]}", end='')
                        if i < len(lines):
                            print(f"{file}:{i+1}: {lines[i]}", end='')

if args.ignorecase:
    for file in args.files:
        with open(file) as f:
            lines = f.readlines()
            patrn = re.compile(args.pattern, re.IGNORECASE)
            for i, line in enumerate(lines, start=1):
                match = patrn.search(line)
                if match:
                    line = re.sub(match.group(),f"{Fore.RED}{match.group()}{Style.RESET_ALL}", line)
                    print(f"{file}:{i}: {line}", end='')

if args.invert:
    for file in args.files:
        with open(file) as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                match = re.search(args.pattern, line)
                if not match:
                    print(f"{file}:{i}: {line}", end='')
