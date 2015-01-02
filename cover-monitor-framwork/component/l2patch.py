# -*- coding: utf-8 -*-
from .component import Component



class L2Patch(Component):
    """docstring for L2Patch"""


    name = "l2patch"
    cmd = "sh -x ./tools/linkbase/seekglobal_l2patch.sh "
