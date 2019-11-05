


global G_lambdaVol_light_G, G_targetVol_light_G
global G_lambdaVol_dark_G, G_targetVol_dark_G
global G_J0_G
global G_J_ll_G, G_J_dd_G, G_J_dl_G, G_J_lm_G, G_J_dm_G

global G_interact_range_G
global G_repeat_G
global G_big_d_G, G_small_d_G
global G_vol_ratio_G, G_lam_vol_ratio_G

G_repeat_G = {{repeat}}#0

G_targetVol_light_G = {{targetVol_light}}#25.0

G_vol_ratio_G = {{vol_ratio}} #constant = 1 for now

G_targetVol_dark_G = G_vol_ratio_G * G_targetVol_light_G # Vtg(D) = eps * Vtg(L)

G_lambdaVol_light_G = {{lambdaVol_light}}#2.0

G_lam_vol_ratio_G = {{lam_vol_ratio}} #constant = 1 for now

G_lambdaVol_dark_G = G_lam_vol_ratio_G * G_lambdaVol_light_G#   lmb_v(D) = eps * lmb_v(L)                                ####{{lambdaVol_dark}}#2.0

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

G_big_d_G = {{big_d}}#2

G_small_d_G = {{small_d}}#1

if abs(G_small_d_G) > G_big_d_G:
    #this way the inequality is satisfied while keeping the number of repetitions
    #correct. 
    if G_small_d_G < 0:
        G_small_d_G = -.9*G_big_d_G 
    else:
        G_small_d_G = .9*G_big_d_G 
G_J0_G = {{J0}}#12

G_J_ll_G = G_J0_G + G_big_d_G

G_J_dl_G = G_J0_G + G_small_d_G

G_J_dd_G = G_J0_G - G_big_d_G

G_J_lm_G = 2*G_J_ll_G

G_J_dm_G = G_J_lm_G





G_interact_range_G = {{interact_range}}#1








def configure_simulation():

    from cc3d.core.XMLUtils import ElementCC3D
    from numpy import sqrt as nsqrt
    
    
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20190906","Version":"4.1.0"})
    
    MetadataElmnt=CompuCell3DElmnt.ElementCC3D("Metadata")
    
    # Basic properties simulation
    MetadataElmnt.ElementCC3D("NumberOfProcessors",{},"1")
    MetadataElmnt.ElementCC3D("DebugOutputFrequency",{},"100")
    # MetadataElmnt.ElementCC3D("NonParallelModule",{"Name":"Potts"})
    
    PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
    
    # Basic properties of CPM (GGH) algorithm
    PottsElmnt.ElementCC3D("Dimensions",{"x":"256","y":"256","z":"1"})
    PottsElmnt.ElementCC3D("Steps",{},"10001")
    PottsElmnt.ElementCC3D("Temperature",{},"10.0")
    PottsElmnt.ElementCC3D("NeighborOrder",{},str(G_interact_range_G))
    
    PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
    
    # Listing all cell types in the simulation
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"dark"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"light"})
    
#     PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
#     PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"dark","LambdaVolume":"2.0","TargetVolume":"50"})
#     PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"light","LambdaVolume":"2.0","TargetVolume":"50"})
    
    PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"dark",
                                                        "LambdaVolume":str(G_lambdaVol_dark_G),
                                                        "TargetVolume":str(G_targetVol_dark_G)})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"light",
                                                        "LambdaVolume":str(G_lambdaVol_light_G),
                                                        "TargetVolume":str(G_targetVol_light_G)})
    
    
    PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"NeighborTracker"})
    
    # Module tracking center of mass of each cell
    
    PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
    # Specification of adhesion energies
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"10.0")
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"dark"},"10.0")
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"light"},"10.0")
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"dark","Type2":"dark"},"10.0")
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"dark","Type2":"light"},"10.0")
#     PluginElmnt_3.ElementCC3D("Energy",{"Type1":"light","Type2":"light"},"10.0")
#     PluginElmnt_3.ElementCC3D("NeighborOrder",{},"4")
    
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"10.0")    
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"dark"},str(G_J_dm_G))
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"light"},str(G_J_lm_G))
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"dark","Type2":"dark"},str(G_J_dd_G))
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"dark","Type2":"light"},str(G_J_dl_G))
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"light","Type2":"light"},str(G_J_ll_G))
    PluginElmnt_3.ElementCC3D("NeighborOrder",{},str(G_interact_range_G))
    
    
    
    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"BlobInitializer"})
    
    # Initial layout of cells in the form of spherical (circular in 2D) blob
    RegionElmnt=SteppableElmnt.ElementCC3D("Region")
#     RegionElmnt.ElementCC3D("Center",{"x":"128","y":"128","z":"0"})
#     RegionElmnt.ElementCC3D("Radius",{},"51")
#     RegionElmnt.ElementCC3D("Gap",{},"0")
#     RegionElmnt.ElementCC3D("Width",{},"7")
#     RegionElmnt.ElementCC3D("Types",{},"dark,light")
    
    RegionElmnt.ElementCC3D("Center",{"x":"128","y":"128","z":"0"})
    RegionElmnt.ElementCC3D("Radius",{},"112")
    RegionElmnt.ElementCC3D("Gap",{},"0")
    RegionElmnt.ElementCC3D("Width",{},str(int(round(nsqrt(G_targetVol_light_G)))))#this way they will be about the right size to begin with
    RegionElmnt.ElementCC3D("Types",{},"dark,light")


    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    

    


        
    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)

            
from cc3d import CompuCellSetup
        

configure_simulation()            

            

from ai_cell_sort_4_pySteppables import ai_cell_sort_4_pySteppable

CompuCellSetup.register_steppable(steppable=ai_cell_sort_4_pySteppable(frequency=10,
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
                                                        _small_d = G_small_d_G,
                                                        _vol_ratio = G_vol_ratio_G,
                                                        _lam_vol_ratio = G_lam_vol_ratio_G))


CompuCellSetup.run()
