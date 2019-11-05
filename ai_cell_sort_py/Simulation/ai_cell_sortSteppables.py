
from PySteppables import *
import CompuCell
import sys
class ai_cell_sortSteppable(SteppableBasePy):

    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        # any code in the start function runs before MCS=0
        pass
    def step(self,mcs):        
        #type here the code that will run every _frequency MCS
        pass
    def finish(self):
        # Finish Function gets called after the last MCS
        pass
        
from PySteppables import *
import CompuCell
import sys

from PlayerPython import *
import CompuCellSetup
import os
import numpy as np

class save_data(SteppableBasePy):
    def __init__(self,_simulator,_frequency,
                  _targetVol_light,_lambdaVol_light,
                  _targetVol_dark,_lambdaVol_dark,
                  _J_ll,_J_dd,_J_dl,_J_lm,_J_dm,
                  _repeat,_interact_range,
                  _big_d, _small_d,
                  _vol_ratio,   _lam_vol_ratio):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        
        #print '=================\n init \n ==================='
        self.targetVol_light = _targetVol_light
        self.lambdaVol_light = _lambdaVol_light
        self.targetVol_dark =_targetVol_dark
        self.lambdaVol_dark = _lambdaVol_dark
        
        self.vol_ratio = _vol_ratio
        self.lam_vol_ratio = _lam_vol_ratio
        
        
        
        self.big_d = _big_d
        self.small_d = _small_d
        self.J_ll = _J_ll
        self.J_dd = _J_dd
        self.J_dl = _J_dl
        self.J_lm = _J_lm
        self.J_dm = _J_dm
        
        self.repeat = _repeat
        self.interact_range = _interact_range
        
    def start(self):
        print "save_data: This function is called once before simulation"
        fileDir = os.path.dirname(os.path.abspath(__file__))
        self.saveDir = os.path.join(fileDir,'data')
        
        if not os.path.isdir(self.saveDir):
            os.makedirs(self.saveDir)
        
        param_name = os.path.join(self.saveDir,'parameters.dat')
        parameters = open(param_name,'w+')
        parameters.write('repeat = ' +str(self.repeat)+
                         '\n interaction range = '+str(self.interact_range)+
                         '\n delta = ' + str(self.small_d) +
                         '\n Delta = ' + str(self.big_d) +
                         '\n J_ll = '+str(self.J_ll)+
                         '\n J_dd = '+str(self.J_dd)+
                         '\n J_dl = '+str(self.J_dl)+
                         '\n J_lm = '+str(self.J_lm)+
                         '\n J_dm = '+str(self.J_dm)+
                         '\n target vol light = ' + str(self.targetVol_light)+
                         '\n lambda vol light = ' + str(self.lambdaVol_light)+
                         '\n target vol dark = ' + str(self.targetVol_dark)+
                         '\n lambda vol dark = ' + str(self.lambdaVol_dark)+
                         '\n volume ratio = ' + str(self.vol_ratio) + 
                         '\n lambda ratio = ' + str(self.lam_vol_ratio)
                         )
        parameters.close()
        self.pos_dir = os.path.join(self.saveDir,'positional')
        if not os.path.isdir(self.pos_dir):
            os.makedirs(self.pos_dir)
        
        con_dir = os.path.join(self.saveDir,'contact')
        if not os.path.isdir(con_dir):
            os.makedirs(con_dir)
        
        self.contact_m_data_dir = os.path.join(con_dir,'contact_means.dat')
        self.contact_m_data = open(self.contact_m_data_dir,'w+')
        self.contact_m_data.write(
                'mcs,LL contact, std,DD contact,std, LD contact,std, ML contact,std, MD contact,std\n')
        
        self.contact_data_dir = os.path.join(con_dir,'contact_totals.dat')
        self.contact_data = open(self.contact_data_dir,'w+')
        self.contact_data.write('mcs,LL contact, DD contact, LD contact, ML contact, MD contact\n')
        
        pop_dir = os.path.join(self.saveDir,'pop_number.dat')
        self.population = open(pop_dir,'w+')
        self.population.write('mcs,# of cells\n')
        
        
    def step(self,mcs):
        
        
        pos_data_name = 'cell_positional_data_'+str(mcs)+'.dat'
        position_data_dir = os.path.join(self.pos_dir,pos_data_name)
        pos_data = open(position_data_dir,'w+')
        pos_data.write('ID,type,x COM, y COM, Same type contact, Oposite type contact, Medium contact\n')
        
        contact_ll = []
        contact_dd = []
        contact_ld = []
        contact_dm = []
        contact_lm = []
        
        for cell in self.cellListByType(self.LIGHT):
            CC = 0 # cell and same type
            CD = 0 # cell and different type
            CM = 0 # cell and medium
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    if neighbor.type == self.LIGHT:
                        contact_ll.append(commonSurfaceArea)
                        CC += commonSurfaceArea
                    elif neighbor.type == self.DARK:
                        contact_ld.append(commonSurfaceArea)
                        CD += commonSurfaceArea
                else:
                    contact_lm.append(commonSurfaceArea)
                    CM += commonSurfaceArea
            # 2 int, 4 float
            pos_data.write('%i,%i,%f,%f,%f,%f,%f\n'%(cell.id,cell.type,cell.xCOM,cell.yCOM,CC,CD,CM))
        
        
        
        for cell in self.cellListByType(self.DARK):  
            CC = 0 # cell and same type
            CD = 0 # cell and different type
            CM = 0 # cell and medium
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    if neighbor.type == self.DARK:
                        contact_dd.append(commonSurfaceArea)
                        CC += commonSurfaceArea
                    elif neighbor.type == self.LIGHT:
                        CD += commonSurfaceArea
                else:
                    contact_dm.append(commonSurfaceArea)  
                    CM += commonSurfaceArea
            # 2 int, 4 float
            pos_data.write('%i,%i,%f,%f,%f,%f,%f\n'%(cell.id,cell.type,cell.xCOM,cell.yCOM,CC,CD,CM))
            
        pos_data.close()
        #self.contact_m_data.write('mcs,LL contact, std,DD contact,std, LD contact,std, ML contact,std, DL contact,std\n')
        # 1 int, 10 float
        self.contact_m_data.write('%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'%(
                                mcs,
                                np.mean(contact_ll),np.std(contact_ll),
                                np.mean(contact_dd),np.std(contact_dd),
                                np.mean(contact_ld),np.std(contact_ld),
                                np.mean(contact_lm),np.std(contact_lm),
                                np.mean(contact_dm),np.std(contact_dm),
                                )
                             )
        
        self.contact_m_data.flush()
        os.fsync(self.contact_m_data)
        
        #self.contact_data.write('mcs,LL contact, DD contact, LD contact, ML contact, DL contact\n')
        #1 int, 5 float
        self.contact_data.write('%i,%f,%f,%f,%f,%f\n'%(
                            mcs,.5*np.sum(contact_ll),.5*np.sum(contact_dd),
                            np.sum(contact_ld),np.sum(contact_lm),np.sum(contact_dm)))
        
        self.contact_data.flush()
        os.fsync(self.contact_data)
        
        
        
        self.population.write('%i,%i\n'%(mcs,len(self.cellList)))
        self.population.flush()
        os.fsync(self.population)
    def finish(self):
        # this function may be called at the end of simulation - used very infrequently though
        self.contact_m_data.close()
        self.contact_data.close()
        self.population.close()
    
