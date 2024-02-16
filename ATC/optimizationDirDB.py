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

class OptimizationDirDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Design optimization',self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        self.form=form
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, OptimizationDirDB.onCmdDone)

        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Method', ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_3 = FXGroupBox(p=TabItem_1, text='', opts=FRAME_GROOVE)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=5, pt=0, pb=0)

        ComboBox_2 = AFXComboBox(p=VAligner_1, ncols=30, nvis=1, text='', tgt=form.keyword19Kw, sel=0, opts=LAYOUT_FILL_X)
        ComboBox_2.setMaxVisible(10)
        ComboBox_2.appendItem(text='Single Objective Genetic Algorithm')
        ComboBox_2.appendItem(text='Multi Objective Genetic Algorithm')

        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Max_function_evaluations  ', opts=JUSTIFY_LEFT)
        l.setTipText("Number of function evaluations allowed for optimizers")
        AFXTextField(p=HFrame_1, ncols=12, labelText='', tgt=form.maxevalKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='population_size ', opts=JUSTIFY_LEFT)
        l.setTipText("Set the initial population size in JEGA methods")
        AFXTextField(p=HFrame_1, ncols=12, labelText='', tgt=form.popsizeKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Seed ', opts=JUSTIFY_LEFT)
        l.setTipText("Seed of the random number generator")
        AFXTextField(p=HFrame_1, ncols=12, labelText='', tgt=form.seedKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Printed_each_pop', opts=JUSTIFY_LEFT)
        l.setTipText("Print every population to a population file")
        AFXTextField(p=HFrame_1, ncols=12, labelText='', tgt=form.printpopKw, sel=0)

        tabItem = FXTabItem(p=TabBook_1, text='Variables', ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # GroupBox = FXGroupBox(p=TabItem_2, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        VAligner_1 = AFXVerticalAligner(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        vf = FXVerticalFrame(VAligner_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 5, 5, 0, 0)

        vf.setSelector(99)
        n = len(globalVar.get_myinitialvalues())
        if len(globalVar.get_myinitialvalues()) == 1:
            n = 16
        tablecoeff = AFXTable(vf, n, 4, n, 4, form.tablecoeffKw, 4, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        tablecoeff.setLeadingRows(1)
        colwidth=80
        tablecoeff.setColumnWidth(0, colwidth-20)
        tablecoeff.setColumnWidth(1, colwidth-20)
        tablecoeff.setColumnWidth(2, colwidth)
        tablecoeff.setColumnWidth(3, colwidth)

        tablecoeff.setColumnType(0, AFXTable.TEXT)
        tablecoeff.setColumnType(1, AFXTable.TEXT)
        tablecoeff.setColumnType(2, AFXTable.INT)
        tablecoeff.setColumnType(3, AFXTable.INT)

        tablecoeff.setLeadingRowLabels('Layer \tName \tLower Bound \tUpper Bound ')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff = tablecoeff


        # self.iv = globalVar.get_myinitialvalues()

        # for i in range(1, len(self.iv)):
        #     GroupBox = FXGroupBox(p=TabItem_2, text='Variable v%s' % self.iv[i], opts=FRAME_GROOVE | LAYOUT_FILL_X)
        #     HFrame_1 = FXHorizontalFrame(p=GroupBox, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
            # AFXTextField(p=HFrame_1, ncols=12, labelText='L ', tgt=form.LKw, sel=i)
            # AFXTextField(p=HFrame_1, ncols=12, labelText='U ', tgt=form.UKw, sel=i)

        tabItem = FXTabItem(p=TabBook_1, text='Responses', ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_1 = FXGroupBox(p=TabItem_3, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        VAligner_3 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=5, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Descriptor   ', opts=JUSTIFY_LEFT)
        l.setTipText("Labels for the responses")
        AFXTextField(p=HFrame_1, ncols=15, labelText='', tgt=form.descriptorKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Sense', opts=JUSTIFY_LEFT)
        l.setTipText("Whether to minimize or maximize each objective function")
        AFXTextField(p=HFrame_1, ncols=15, labelText='', tgt=form.senseKw, sel=0)
        #VAligner_4 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=5, pt=0, pb=0)

        GroupBox_1 = FXGroupBox(p=TabItem_3, text='Inequality Constraints', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Descriptor     ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_1, ncols=12, labelText='', tgt=form.ineq_descriptorKw, sel=0)
        HFrame_2 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_2, text='Upper Bound', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_2, ncols=12, labelText='', tgt=form.upperboundKw, sel=0)

        ComboBox_2 = AFXComboBox(p=VAligner_3, ncols=12, nvis=2, text='Nodal Set  =  ', tgt=form.nodesetKw, sel=0, opts=LAYOUT_FILL_X)
        ComboBox_2.setMaxVisible(5)
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        for i in mdb.models[modelName].rootAssembly.sets.keys():
            ComboBox_2.appendItem(text=i)

        # HFrame_4 = FXHorizontalFrame(p=VAligner_3, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, opts=LAYOUT_FILL_X)
        # fileHandler = BbDBFileHandler(form, 'jobname', '*.inp')
        # fileTextHf = FXHorizontalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # # Note: Set the selector to indicate that this widget should not be
        # #       colored differently from its parent when the 'Color layout managers'
        # #       button is checked in the RSG Dialog Builder dialog.
        # fileTextHf.setSelector(99)
        # AFXTextField(p=fileTextHf, ncols=15, labelText='Jobname  =  ', tgt=form.jobnameKw, sel=0, opts=AFXTEXTFIELD_STRING | LAYOUT_CENTER_Y)
        # FXButton(p=fileTextHf, text=' .inp ', tgt=fileHandler, sel=AFXMode.ID_ACTIVATE, opts=BUTTON_NORMAL | LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)


    def onCmdDone(self, sender, sel, ptr):
        
            
        # get current working file name
        a = globalVar.get_myabq_job()[0]
        blocks = a.split('/')
        jobname = blocks[-1]
        
        with open(jobname) as b:
            lines = b.readlines()

        for i in range(0, len(lines)):
            if lines[i] == "*End Part\n":
                lines.insert(i, "*Include, input=shellsections.inp\n")
                break

        with open(jobname, "w") as b:
            b.writelines(lines)
        b.close()
        
        
        
        # write arguments in post process part
        args = globalVar.get_myabq_arg()
        f = open(jobname + "args.txt", "w")
        f.write(str(globalVar.get_myabq_name()[0]) + '\n')
        f.write(str(globalVar.get_myabq_script()[0]) + '\n')
        f.write(str(args) + '\n')
        f.write(str(globalVar.get_myabq_step_result()[0]) + '\n')
        f.close()
        
        # write method in optimization
        paras_opti = []
        paras_opti.append([str(self.form.maxevalKw.getValue()), str(self.form.popsizeKw.getValue()), str(self.form.seedKw.getValue()), str(self.form.printpopKw.getValue())])
        f = open(jobname + "method_opti.txt", "w")
        f.write(str(paras_opti) + '\n')
        f.close()
        
        # write variable in optimization
        var_dump_coef = []
        for i in range(1, self.tablecoeff.getNumRows()):
            if self.tablecoeff.getItemText(i, 0) != '':
                var_dump_coef.append([self.tablecoeff.getItemText(i, 0), self.tablecoeff.getItemText(i, 1), self.tablecoeff.getItemText(i, 2), self.tablecoeff.getItemText(i, 3)])
        f = open(jobname + "bounds_opti.txt", "w")
        f.write(str(var_dump_coef) + '\n')
        f.close()
        
        # write response in optimization
        
        response_opti = []
        response_opti.append([self.form.descriptorKw.getValue(), str(self.form.senseKw.getValue())])
        f = open(jobname + "response_opti.txt", "w")
        f.write(str(response_opti) + '\n')
        f.close()
        
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
        
        
        
        with open('Paths.txt') as inp:
            lines = inp.readlines()
        sys_path = lines[0]
        py_path = lines[1]


        os.environ["PYTHONPATH"] = py_path
        os.environ["PATH"] = sys_path
        
        currentWD = os.getcwd()
        
        if 2 not in choice:
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML.py abaqus_op ' +jobname)
        else:
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML-cyl.py abaqus_op ' +jobname)
        
        os.system('datc vs_design_op.yml')
        
        
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)


###########################################################################
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
