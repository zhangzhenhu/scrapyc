# -*- coding: utf-8 -*-
from .component import Component



class Robots(Component):
    """docstring for Robots"""

    name = "robots"
    cmd = "sh -x ./tools/dns/robots.sh "
