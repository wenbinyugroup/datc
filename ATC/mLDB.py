from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar

from mlbo_plugin import Mlbo_plugin
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class MLDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form
        AFXDataDialog.__init__(self, form, 'Training',
            self.OK|AFXMode.ID_ACTIVATE, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Apply')
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, MLDB.onCmdDone)

        # applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        # applyBtn.setText('Advanced')
        
        ML_BO = getAFXApp().getAFXMainWindow().getPluginToolset()
        self.appendActionButton('Advanced', Mlbo_plugin(ML_BO), AFXMode.ID_ACTIVATE)
        
        canBtn = self.appendActionButton(self.CANCEL)
        canBtn.setTipText('Close the current window')
            
        VAligner_3 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_3, ncols=20, labelText='Nerual network        ', tgt=form.NN_mlKw, sel=0)
        AFXTextField(p=VAligner_3, ncols=20, labelText='Optimizer', tgt=form.Opti_mlKw, sel=0)
        AFXTextField(p=VAligner_3, ncols=20, labelText='Learning rate', tgt=form.lr_mlKw, sel=0)
        AFXTextField(p=VAligner_3, ncols=20, labelText='Epochs', tgt=form.epoch_mlKw, sel=0)

    def onCmdDone(self, sender, sel, ptr):
       
        jobname = globalVar.get_myabq_job_ml()[0]
        
        f = open(jobname + "ML_paras.txt", "w")
        f.write(str(self.form.NN_mlKw.getValue())+'\n')
        f.write(str(self.form.Opti_mlKw.getValue())+'\n')
        f.write(str(self.form.lr_mlKw.getValue())+'\n')
        f.write(str(self.form.epoch_mlKw.getValue()))
        f.close()
        
        with open('Paths.txt') as inp:
            lines = inp.readlines()
        sys_path = lines[0]
        py_path = lines[1]

        os.environ["PYTHONPATH"] = py_path
        os.environ["PATH"] = sys_path
        
        cwd = os.getcwd()
        
        os.system('python '+ cwd +'\\PyML\\TrainML.py')
        
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)
    