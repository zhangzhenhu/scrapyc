# -*- coding: utf-8 -*-
from .component import Component



class PCCcdb(Component):
    """docstring for PCCcdb"""


    name = "pcccdb"
    cmd = "sh -x ./tools/wdbtools/seekglobal_multi.sh "
