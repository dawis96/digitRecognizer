# Copyright (c) 2019 Damian Grzywna
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib/

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "aptiv.digitRecognizer"
__summary__      = "Small application to recognize handwritten digits on the image using machine learning algorithm."
__uri__          = "https://github.com/dawis96/digitRecognizer"
__version_info__ = type("version_info", (), dict(serial=0,
                        major=0, minor=1, micro=0, releaselevel="alpha"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Damian Grzywna"
__maintainer__   = "Damian Grzywna"
__email__        = "dawis996@gmail.com"
__copyright__    = "Copyright (c) 2019, {0}".format(__author__)
__license__      = "zlib/libpng License ; {0}".format(
                   "http://opensource.org/licenses/zlib/")
