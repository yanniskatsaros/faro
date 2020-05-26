#!/usr/bin/env python3

"""
Script to generate setup.py file using poetry as the build system
for backwards compatability and local development. Adapted from:

https://github.com/sdss/flicamera/blob/master/create_setup.py

"""

import os
import sys
from pathlib import Path

link = 'https://python-poetry.org/docs/#installation'
try:
    from poetry.masonry.builders.sdist import SdistBuilder
    from poetry.factory import Factory
except:
    raise ImportError(f'Poetry installation missing: install using `pip3 install poetry` or see: {link}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise RuntimeError('usage: python3 make_setup.py path/to/generate/setup.py')

    # generate a Poetry object that knows about metadata in pyproject.toml
    PROJECT_PATH = Path(os.path.dirname(__file__)).resolve().parent
    factory = Factory()
    poetry = factory.create_poetry(PROJECT_PATH)

    # use the builder to generate a blob for setup.py
    builder = SdistBuilder(poetry, None, None)
    setup_blob = builder.build_setup()

    with open(sys.argv[1], 'wb') as f:
        f.write(b'# setup.py automatically generated using poetry\n')
        f.write(setup_blob)
