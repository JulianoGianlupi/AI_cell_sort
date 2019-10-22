
def configureSimulation(sim):
    import CompuCellSetup
    from XMLUtils import ElementCC3D
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20190430","Version":"3.7.9"})
    
    PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
    
    # Basic properties of CPM (GGH) algorithm
    PottsElmnt.ElementCC3D("Dimensions",{"x":"100","y":"100","z":"1"})
    PottsElmnt.ElementCC3D("Steps",{},"1000")
    PottsElmnt.ElementCC3D("Temperature",{},"10.0")
    PottsElmnt.ElementCC3D("NeighborOrder",{},"1")
    
    PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
    
    # Listing all cell types in the simulation
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"cell2"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"cell1"})
    
    PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"cell2","LambdaVolume":"2.0","TargetVolume":"25"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"cell1","LambdaVolume":"2.0","TargetVolume":"25"})
    
    PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    
    # Module tracking center of mass of each cell
    
    PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
    # Specification of adhesion energies
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"10.0")
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"cell2"},"10.0")
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"cell1"},"10.0")
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"cell2","Type2":"cell2"},"10.0")
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"cell2","Type2":"cell1"},"10.0")
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"cell1","Type2":"cell1"},"10.0")
    PluginElmnt_3.ElementCC3D("NeighborOrder",{},"1")
    
    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"BlobInitializer"})
    
    # Initial layout of cells in the form of spherical (circular in 2D) blob
    RegionElmnt=SteppableElmnt.ElementCC3D("Region")
    RegionElmnt.ElementCC3D("Center",{"x":"50","y":"50","z":"0"})
    RegionElmnt.ElementCC3D("Radius",{},"20")
    RegionElmnt.ElementCC3D("Gap",{},"0")
    RegionElmnt.ElementCC3D("Width",{},"5")
    RegionElmnt.ElementCC3D("Types",{},"cell2,cell1")

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    
    


            
    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)
            
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup


sim,simthread = CompuCellSetup.getCoreSimulationObjects()
        
configureSimulation(sim)            
            
# add extra attributes here
        
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from test_pythonSteppables import test_pythonSteppable
steppableInstance=test_pythonSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(steppableInstance)
        
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        