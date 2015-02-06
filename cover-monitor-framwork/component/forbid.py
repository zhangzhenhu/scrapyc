# -*- coding: utf-8 -*-
from .component import Component



class Forbid(Component):
    """docstring for IPForbid"""

    name = "forbid"
    cmd = "sh -x  ./tools/cc_forbid/run.sh"
