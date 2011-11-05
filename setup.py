#! /usr/bin/env python

import os
from distutils.core import setup

setup(name='hamlet',
      version='1.0',
      description='SML interpreter layer',
      author='Truls Edvard Stokke',
      author_email='trulses@gmail.com',
      packages=['smlnj', 'smlnj.util'],
      scripts=['hamlet'])
