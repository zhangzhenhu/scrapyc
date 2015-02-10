# -*- coding: utf-8 -*-
from .component import Component



class WiseCcdb(Component):
    """docstring for WiseCcdb"""


    name = "wiseccdb"
    cmd = "sh -x ./tools/wdbtools/seekglobalwise.sh "
