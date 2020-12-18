import io
import sys

for line in io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='ignore'):
    try:
        # remove null
        line = line.replace('\x00','')
        sys.stdout.write(line)
    except:
        sys.stdout.write('\n')
