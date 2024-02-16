from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar
import json

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

###########################################################################
# Class definition
###########################################################################

class StructuralDirDB(AFXDataDialog):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form
        self.eqs=globalVar.get_myeqs()
        AFXDataDialog.__init__(self, form, 'Structural Analysis', self.OK | self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        # okBtn = self.getActionButton(self.ID_CLICKED_OK)
        # okBtn.setText('Done')
        GroupBox_4 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        HFrame_4 = FXHorizontalFrame(p=GroupBox_4, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, opts=LAYOUT_FILL_X)
        fileHandler = BbDBFileHandler(form, 'jobname', '*.inp')
        fileTextHf = FXHorizontalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0,
                                       hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=30, labelText='Jobname  =  ', tgt=form.jobnameKw, sel=0,
                     opts=AFXTEXTFIELD_STRING | LAYOUT_CENTER_Y)
        FXButton(p=fileTextHf, text=' .inp ', tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)

        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place = LAYOUT_SIDE_BOTTOM | LAYOUT_SIDE_RIGHT
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK,StructuralDirDB.onCmdDone)
        
    def onCmdDone(self, sender, sel, ptr):

        a = self.form.jobnameKw.getValue()
        blocks = a.split('/')
        for i in blocks:
            if '.inp' in i:
                jobname = i
                
        with open(jobname) as b:
            lines = b.readlines()

        for i in range(0, len(lines)):
            if lines[i] == "*End Part\n":
                lines.insert(i, "*Include, input=shellsections.inp\n")
                break

        with open(jobname, "w") as b:
            b.writelines(lines)
        b.close()

        f = open(jobname+"LaminaProp_adv_SA.txt", "w")
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm = mdb.models[modelName].materials

        for mat_name in list(set(globalVar.get_mymaterial())):
            for i in cm[mat_name].elastic.table:
                for j in i:
                    f.write(str(j) + '\n')
            # for i in cm[mat_name].expansion.table:
                # for j in i:
                    # f.write(str(j) + '\n')

        f.close()
        
        # write design variables and its initial values
        f = open(jobname+"DesignVariable_ply.txt", "w")
        f.write(str(globalVar.get_IV_designVar()) + '\n')
        f.close()
        
        # write design variables and its initial values
        f = open(jobname+"DesignVariable_fp.txt", "w")
        f.write(str(globalVar.get_IV_thickEQN()) + '\n')
        f.close()
        
        # write layer information and layup
        f = open(jobname+"LayupandLayerinfo.txt", "w")
        
        f.write(str(globalVar.get_mylayup()) + '\n')
        for i, j in globalVar.Layer().get_defineFiberAngles().items():
            f.write((i) + '\n')
            f.write((j['type']) + '\n')
            f.write(str(j['ply_thickness']) + '\n')
            f.write(str(j['orientation']) + '\n')
        
        f.close()
        
        
        dict2=globalVar.get_thisdict()
        dict1=dict2
        choice = globalVar.get_mychoicelist()
        
        
        f = open(jobname + "all_funcScripts.txt", "w")
        
        # f.write(str(choice))
        for i in range(0, len(choice)):
            if choice[i] == 2:
                f.write(str(globalVar.get_mylid()[i]) + '\n')
                f.write(str(dict1["file"][0]) + '\n')
                f.write(str(dict1["function"][0]) + '\n')
                for j in range(0, len(dict1["coeffname"][0])):  #
                    f.write(str(dict1["coeffname"][0][j])+' ')
                    f.write(str(dict1["coeffval"][0][j])+'\n')
                    
                f.write(str(dict1["m"][0]) + '\n')
                # dict1['file'].remove(dict1['file'][0])
                # dict1['function'].remove(dict1['function'][0])
                # dict1['transformation'].remove(dict1['transformation'][0])
                # dict1['coeffval'].remove(dict1['coeffval'][0])
                # dict1['coeffname'].remove(dict1['coeffname'][0])
                # dict1['m'].remove(dict1['m'][0])
        f.close()
        
        # import shutil
        # if os.path.exists(jobname):
            # cwd = os.getcwd()
            # src = cwd + '\\' + jobname
            # dst = cwd + '\\model\\' + jobname
            # shutil.copyfile(src, dst)

        with open('Paths.txt') as inp:
            lines = inp.readlines()
        sys_path = lines[0]
        py_path = lines[1]


        os.environ["PYTHONPATH"] = py_path
        os.environ["PATH"] = sys_path
        
        currentWD = os.getcwd()
        # print('*'*23)
        # print(currentWD)
        # print('*'*23)
        
        
        if 2 not in choice:
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML.py abaqus_sa ' +jobname)
        else:
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML-cyl.py abaqus_sa ' +jobname)
        
        os.system('datc vs_design_sa.yml')
        

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

# Class definition
###########################################################################

class BbDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.jobnameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, BbDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.jobnameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.inp')
       fileDb.create()
       fileDb.showModal()