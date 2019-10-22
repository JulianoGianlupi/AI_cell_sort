

global G_lambdaVol_light_G, G_targetVol_light_G
global G_lambdaVol_dark_G, G_targetVol_dark_G
global G_J0_G
global G_J_ll_G, G_J_dd_G, G_J_dl_G, G_J_lm_G, G_J_dm_G

global G_interact_range_G
global G_repeat_G
global G_big_d_G, G_small_d_G

G_repeat_G = 0

G_targetVol_light_G = 25.0
G_targetVol_dark_G = G_targetVol_light_G #to begin with

G_lambdaVol_light_G = 2.0
G_lambdaVol_dark_G = 2.0

'''
* J(L,M) = J(d,M)

* J(L,M) > J(l,l)  => J(l,m) = 2 J(l,l)

* J(l,l) > J(d,l)

* J(d,l) > 0.5 * [ J(d,d)+J(l,l) ] 

* 0.5 * [ J(d,d)+J(l,l) ] > J (d,d)  

* ~~J (d,d) > 0~~ not necessary (if I recall correctly)

________

J(l,l) = J0 + Delta (ie, + G_big_d_G)

J(l,d) = J0 + delta (ie, + G_small_d_G)

J(d,d) = J0 - Delta 

Delta > 0; - Delta < delta <  Delta 

'''

G_big_d_G = 2

G_small_d_G = 1

if abs(G_small_d_G) > G_big_d_G:
    #this way the inequality is satisfied while keeping the number of repetitions
    #correct. 
    if G_small_d_G < 0:
        G_small_d_G = -.9*G_big_d_G 
    else:
        G_small_d_G = .9*G_big_d_G 
G_J0_G = 12

G_J_ll_G = G_J0_G + G_big_d_G

G_J_dl_G = G_J0_G + G_small_d_G

G_J_dd_G = G_J0_G - G_big_d_G

G_J_lm_G = 2*G_J_ll_G

G_J_dm_G = G_J_lm_G





G_interact_range_G = 1


def configureSimulation(sim):
    import CompuCellSetup
    from XMLUtils import ElementCC3D
    from numpy import sqrt as nsqrt
    
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20190430","Version":"3.7.9"})
    
    PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
    PottsElmnt.ElementCC3D("Dimensions",{"x":"256","y":"256","z":"1"})
    PottsElmnt.ElementCC3D("Steps",{},"50000")
    PottsElmnt.ElementCC3D("Temperature",{},"10.0")
    PottsElmnt.ElementCC3D("NeighborOrder",{},str(G_interact_range_G))
    
    
    PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"dark"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"light"})
    
    
    PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"dark",
                                                        "LambdaVolume":str(G_lambdaVol_dark_G),
                                                        "TargetVolume":str(G_targetVol_dark_G)})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"light",
                                                        "LambdaVolume":str(G_lambdaVol_light_G),
                                                        "TargetVolume":str(G_targetVol_light_G)})
    
    CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"NeighborTracker"})
    
    PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"10.0")    
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"dark"},str(G_J_dm_G))
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"light"},str(G_J_lm_G))
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"dark","Type2":"dark"},str(G_J_dd_G))
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"dark","Type2":"light"},str(G_J_dl_G))
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"light","Type2":"light"},str(G_J_ll_G))
    PluginElmnt_2.ElementCC3D("NeighborOrder",{},str(G_interact_range_G))
    
   
    
    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"BlobInitializer"})
    RegionElmnt=SteppableElmnt.ElementCC3D("Region")
    RegionElmnt.ElementCC3D("Center",{"x":"128","y":"128","z":"0"})
    RegionElmnt.ElementCC3D("Radius",{},"112")
    RegionElmnt.ElementCC3D("Gap",{},"0")
    RegionElmnt.ElementCC3D("Width",{},str(int(round(nsqrt(G_targetVol_light_G)))))#this way they will be about the right size to begin with
    RegionElmnt.ElementCC3D("Types",{},"dark,light")
    
    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    
    
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup

sim,simthread = CompuCellSetup.getCoreSimulationObjects()
# add extra attributes here
configureSimulation(sim)              
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
from ai_cell_sortSteppables import ai_cell_sortSteppable
steppableInstance=ai_cell_sortSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(steppableInstance)
        
from ai_cell_sortSteppables import save_data
instanceOfsave_data=save_data(_simulator=sim,_frequency=10,
                              _targetVol_light = G_targetVol_light_G,
                              _lambdaVol_light = G_lambdaVol_light_G,
                              _targetVol_dark = G_targetVol_dark_G,
                              _lambdaVol_dark = G_lambdaVol_dark_G,
                              _J_ll = G_J_ll_G,
                              _J_dd = G_J_dd_G,
                              _J_dl = G_J_dl_G,
                              _J_lm = G_J_lm_G,
                              _J_dm = G_J_dm_G,
                              _repeat = G_repeat_G,
                              _interact_range = G_interact_range_G,
                              _big_d = G_big_d_G,
                              _small_d = G_small_d_G)

steppableRegistry.registerSteppable(instanceOfsave_data)
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        