# Copyright (c) 2019 Damian Grzywna
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib/


def make_config(cfg_name, cfg_section):

    import sys
    from os import path

    fglobals = sys._getframe(1).f_globals
    cfg_path = path.join(path.dirname(fglobals["__file__"]), cfg_name)
    fglobals["config"] = get_config(cfg_path, cfg_section)
    fglobals.pop("__builtins__", None)
    fglobals.pop("__cached__",   None)
    fglobals["__all__"] = ("config",)


def get_config(cfg_path, cfg_section):

    from os import path
    from configparser import ConfigParser, ExtendedInterpolation

    if not path.isfile(cfg_path):
        return {}

    cfg = ConfigParser(interpolation=ExtendedInterpolation(),
                       inline_comment_prefixes=('#', ';'),
                       default_section=cfg_section)
    cfg.read(cfg_path, "utf-8")
    return cfg[cfg_section]
