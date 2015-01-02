
import os

WORDIR=os.getcwd()
JOBDIR = os.path.join(WORDIR,"history")


COMPONENTS = {
    "component.pcccdb.PCCcdb" :None,
    "component.linkbase.Linkbase" :None,
    "component.wiseccdb.WiseCcdb" :None,
    "component.l2linkbase.L2base" :None,
    "component.l2patch.L2Patch" :None,
    # "component.robots" :None,
    # "component.dc" :None,
} 
STRATEGIES = [
    "strategy.ccdb.CCDB",
    "strategy.linkbase.Linkbase",
    "strategy.close.Close",
    "strategy.output.Output",
    "strategy.statistic.Statistic",
    # "strategy.weight":None,
    # "strategy.valid":None,
    
]