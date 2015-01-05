# -*- coding: utf-8 -*-
from .levelselect import LevelSelect



class LevelAll(LevelSelect):
    """docstring for LevelAll"""


    name = "level_all"
    cmd = "sh -x ./tools/select/get_prefixt_stat_intps.sh level_all"
