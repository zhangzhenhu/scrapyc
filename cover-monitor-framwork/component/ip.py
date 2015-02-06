# -*- coding: utf-8 -*-
from .component import Component



class IP(Component):
    """docstring for Linkbase"""

    name = "ip"
    cmd = "sh -x ./tools/cc_ip/run.sh"
