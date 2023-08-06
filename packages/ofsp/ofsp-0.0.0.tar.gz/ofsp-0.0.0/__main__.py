#! /usr/bin/env python3

import subprocess
import sys


def bootstrap():
    pass


def squash(input_root):
    subprocess.call([
        'mksquashfs',
        input_root,
        ?,
        '-comp', 'zstd',
        '-Xcompression-level', str(18),
    ])


def main():
    _, output_root = sys.argv
    bootstrap()
    squash()
    print('ok')


if __name__ == '__main__':
    main()
