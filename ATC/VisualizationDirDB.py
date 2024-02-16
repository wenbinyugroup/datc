from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

###########################################################################
# Class definition
###########################################################################

class VisualizationDirDB(AFXDataDialog):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        
        AFXDataDialog.__init__(self, form, 'Visual',self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')
            
        GroupBox_1 = FXGroupBox(p=self, text='V1', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='k1', tgt=form.k1Kw, sel=0)
        