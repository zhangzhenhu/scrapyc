
from .component import Component



class Robots(Component):
    """docstring for Robots"""

    name = "robots"
    cmd = "sh -x ./tools/forbid/robots.sh "
