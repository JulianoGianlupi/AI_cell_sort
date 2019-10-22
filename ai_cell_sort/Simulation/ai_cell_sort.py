
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup


sim,simthread = CompuCellSetup.getCoreSimulationObjects()
        
# add extra attributes here
        
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from ai_cell_sortSteppables import ai_cell_sortSteppable
steppableInstance=ai_cell_sortSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(steppableInstance)
        

from ai_cell_sortSteppables import save_data
instanceOfsave_data=save_data(_simulator=sim,_frequency=10)
steppableRegistry.registerSteppable(instanceOfsave_data)

CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        