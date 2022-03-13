# Adapted from https://github.com/skogsbaer/check-assignments/blob/main/src/fixEncodingCmd.py

import sys

extensions = ['.java', '.py', '.hs']
replacements = ['ä', 'ö', 'ü', 'Ä', 'Ö', 'Ü', 'ß']


def fix(path):
    bytes_orig = open(path, 'rb').read()
    bytes = bytes_orig
    for r in replacements:
        bytes = bytes.replace(r.encode('iso-8859-1'), r.encode('utf-8'))
    if bytes != bytes_orig:
        open(path, 'wb').write(bytes)
        print(f'Fixed encoding of {path}')


if __name__ == '__main__':
    for path in sys.argv[1:]:
        for ext in extensions:
            if path.endswith(ext):
                fix(path)
