
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
    def __init__(self,_simulator,_frequency=10):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        
    def start(self):
        print "save_data: This function is called once before simulation"
        fileDir = os.path.dirname(os.path.abspath(__file__))
        self.saveDir = os.path.join(fileDir,'data')
        
        if not os.path.isdir(self.saveDir):
            os.makedirs(self.saveDir)
        
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
        
    def step(self,mcs):
        
        
        pos_data_name = 'cell_positional_data_'+str(mcs)+'.dat'
        position_data_dir = os.path.join(self.pos_dir,pos_data_name)
        pos_data = open(position_data_dir,'w+')
        pos_data.write('ID,type,x COM, y COM\n')
        
        contact_ll = []
        contact_dd = []
        contact_ld = []
        contact_dm = []
        contact_lm = []
        
        for cell in self.cellListByType(self.LIGHT):
            # 2 int, 2 float
            pos_data.write('%i,%i,%f,%f\n'%(cell.id,cell.type,cell.xCOM,cell.yCOM))
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    if neighbor.type == self.LIGHT:
                        contact_ll.append(commonSurfaceArea)
                    elif neighbor.type == self.DARK:
                        contact_ld.append(commonSurfaceArea)
                else:
                    contact_lm.append(commonSurfaceArea)
        
        for cell in self.cellListByType(self.DARK):  
            pos_data.write('%i,%i,%f,%f\n'%(cell.id,cell.type,cell.xCOM,cell.yCOM))
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    if neighbor.type == self.DARK:
                        contact_dd.append(commonSurfaceArea)
                else:
                    contact_dm.append(commonSurfaceArea)    
            
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
        
    def finish(self):
        # this function may be called at the end of simulation - used very infrequently though
        self.contact_m_data.close()
        self.contact_data.close()
    
