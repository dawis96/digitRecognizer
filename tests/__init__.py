# Copyright (c) 2019 Damian Grzywna
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib/

__all__ = ('top_dir', 'test_dir')

import sys, os
sys.dont_write_bytecode = True
test_dir = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.dirname(test_dir)
del sys, os

__all__ += ()
