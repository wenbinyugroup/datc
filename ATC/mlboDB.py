from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class MlboDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form

        AFXDataDialog.__init__(self, form, 'Bayesian optimization',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, MlboDB.onCmdDone)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Apply')
            
        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_1, ncols=12, labelText='Initial points           ', tgt=form.IP_BOKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=12, labelText='Iterations', tgt=form.Iter_BOKw, sel=0)

    def onCmdDone(self, sender, sel, ptr):
       
        jobname = globalVar.get_myabq_job_ml()[0]
        
        f = open(jobname + "BOparas.txt", "w")
        f.write(str(self.form.IP_BOKw.getValue())+'\n')
        f.write(str(self.form.Iter_BOKw.getValue()))
        f.close()
        
        with open('Paths.txt') as inp:
            lines = inp.readlines()
        sys_path = lines[0]
        py_path = lines[1]

        os.environ["PYTHONPATH"] = py_path
        os.environ["PATH"] = sys_path
        
        cwd = os.getcwd()

        os.system('python '+ cwd +'\\PyML\\BOforGUI.py')
        
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)