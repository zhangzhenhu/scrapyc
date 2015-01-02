# -*- coding: utf-8 -*-
from .component import Component



class UA(Component):
    """docstring for Linkbase"""

    name = "ua"
    cmd = "sh -x ./tools/forbid/ua.sh "
