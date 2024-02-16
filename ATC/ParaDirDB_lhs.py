from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar
from showParaForm import ShowParaForm
import json

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class ParaDirDB_lhs(AFXDataDialog):
    [
        ID_MAT,
        ID_INCLUSION_MAT,
        ID_SHOW,
        ID_FIBER
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST + 4)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form

        AFXDataDialog.__init__(self, form, 'Parametric study', self.OK, DIALOG_ACTIONS_SEPARATOR)
        self.eqs = globalVar.get_myeqs()

        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place = LAYOUT_SIDE_BOTTOM | LAYOUT_SIDE_RIGHT

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, ParaDirDB_lhs.onCmdDone)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_MAT, ParaDirDB_lhs.onCmdMAT)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INCLUSION_MAT, ParaDirDB_lhs.onCmdFiberMAT)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_FIBER, ParaDirDB_lhs.onCmdMATRIX)

        canBtn = self.appendActionButton(self.CANCEL)
        canBtn.setTipText('Close the current window')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # tab1
        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
                              opts=TABBOOK_NORMAL,
                              x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                              pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Fiber path', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)

        tablecoeff = AFXTable(vf, 12, 5, 100, 5, form.tablecoeffKw, 4, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        tablecoeff.setLeadingRows(1)
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        tablecoeff.setLeadingColumns(1)
        tablecoeff.setColumnWidth(1, 60)
        tablecoeff.setColumnType(1, AFXTable.TEXT)
        tablecoeff.setColumnWidth(2, 60)
        tablecoeff.setColumnType(2, AFXTable.TEXT)
        tablecoeff.setColumnWidth(3, 80)
        tablecoeff.setColumnType(3, AFXTable.INT)
        tablecoeff.setColumnWidth(4, 80)
        tablecoeff.setColumnType(4, AFXTable.INT)
        # tablecoeff.setColumnWidth(5, 60)
        # tablecoeff.setColumnType(5, AFXTable.INT)

        tablecoeff.setLeadingRowLabels('Layer\tVariables\tLower Bound\tUpper Bound')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff = tablecoeff
        
        if isinstance(TabItem_1, FXHorizontalFrame):
            FXVerticalSeparator(p=TabItem_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=TabItem_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        AFXTextField(p=TabItem_1, ncols=13, labelText='Number of samples:', tgt=form.NumsampleKw, sel=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # tab 2
        tabItem = FXTabItem(p=TabBook_1, text='Materials', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        TabItem_2 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_1 = FXGroupBox(p=TabItem_2, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)

        FXRadioButton(p=GroupBox_1, text='Materials by user: ', tgt=form.lamina_microscaleKw, sel=1)

        GroupBox_2 = FXGroupBox(p=GroupBox_1, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        FXRadioButton(p=GroupBox_1, text='Materials by microstructure:', tgt=form.lamina_microscaleKw, sel=2)
        self.GroupBox_2 = GroupBox_2
        HFrame_1 = FXHorizontalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)
        ComboBox_2 = AFXComboBox(p=HFrame_1, ncols=15, nvis=1, text='Select material                   ',
                                 tgt=form.laminamaterialKw, sel=0)
        ComboBox_2.setMaxVisible(10)

        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm = mdb.models[modelName].materials
        for i in cm.keys():
            ComboBox_2.appendItem(text=i)

        FXButton(p=HFrame_1, text='Add', tgt=self, sel=self.ID_MAT,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_Y | JUSTIFY_LEFT, x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        GroupBox_3 = FXGroupBox(p=GroupBox_1, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        self.GroupBox_3 = GroupBox_3
        VFrame_1 = FXVerticalFrame(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
                                   pl=0, pr=0, pt=0, pb=0)
        HFrame_2 = FXHorizontalFrame(p=VFrame_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)

        ComboBox_3 = AFXComboBox(p=HFrame_2, ncols=15, nvis=1, text='Fiber material                    ',
                                 tgt=form.inclusionmaterialKw, sel=0)
        ComboBox_3.setMaxVisible(10)
        for i in cm.keys():
            ComboBox_3.appendItem(text=i)

        FXButton(p=HFrame_2, text='Add', tgt=self, sel=self.ID_INCLUSION_MAT,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_Y | JUSTIFY_LEFT, x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        HFrame_3 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)
        ComboBox_4 = AFXComboBox(p=HFrame_3, ncols=15, nvis=1, text='Matrix material                  ',
                                 tgt=form.matrixmaterialKw, sel=0)
        ComboBox_4.setMaxVisible(10)
        for i in cm.keys():
            ComboBox_4.appendItem(text=i)

        FXButton(p=HFrame_3, text='Add', tgt=self, sel=self.ID_FIBER,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_Y | JUSTIFY_LEFT, x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        # AFXTextField(p=VFrame_1, ncols=15, labelText='Inclusion Radius                       ', tgt=form.inclusion_radiusKw, sel=0)
        AFXTextField(p=VFrame_1, ncols=15, labelText='Fiber radius                        ',
                     tgt=form.inclusion_radiusKw, sel=0)
        self.ps_radius = FXCheckButton(p=VFrame_1, text='Parametric study of radius', tgt=self, sel=55,
                                       opts=CHECKBUTTON_NORMAL, x=0,
                                       y=0,
                                       w=0, h=0, pl=DEFAULT_PAD,
                                       pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        # l = FXLabel(p=VFrame_1, text='Inclusion radius:', opts=JUSTIFY_LEFT)
        # l.setTipText("Inclusion radius and its bounds")

        vf = FXVerticalFrame(GroupBox_3, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        vf.setSelector(99)
        table_rad = AFXTable(vf, 3, 3, 100, 3, form.fiber_radius_tableKw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table_rad.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW)
        table_rad.setLeadingRows(1)
        table_rad.setLeadingColumns(1)
        table_rad.setColumnWidth(1, 100)
        table_rad.setColumnType(1, AFXTable.FLOAT)
        table_rad.setColumnWidth(2, 100)
        table_rad.setColumnType(2, AFXTable.FLOAT)
        # table_rad.setColumnWidth(3, 100)
        # table_rad.setColumnType(3, AFXTable.FLOAT)
        # table.setColumnWidth(4, 90)
        # table.setColumnType(4, AFXTable.FLOAT)
        table_rad.setLeadingRowLabels('Lower bound\tUpper bound')
        table_rad.setStretchableColumn(table_rad.getNumColumns() - 1)
        table_rad.showHorizontalGrid(True)
        table_rad.showVerticalGrid(True)
        self.table_rad = table_rad

        Show_new = getAFXApp().getAFXMainWindow().getPluginToolset()

        FXButton(p=GroupBox_1, text='Show', tgt=ShowParaForm(Show_new), sel=AFXMode.ID_ACTIVATE,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_X, x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        # self.appendActionButton('Show', ShowParaForm(Show_new), AFXMode.ID_ACTIVATE)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # tab 3
        tabItem = FXTabItem(p=TabBook_1, text='Plies', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_6 = FXGroupBox(p=TabItem_3, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        self.GroupBox_6 = GroupBox_6
        vf = FXVerticalFrame(GroupBox_6, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table_plies = AFXTable(vf, 12, 5, 100, 5, form.pliesKw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table_plies.setPopupOptions(
            AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW)
        table_plies.setLeadingRows(1)
        table_plies.setLeadingColumns(1)
        table_plies.setColumnWidth(1, 50)
        table_plies.setColumnType(1, AFXTable.INT)
        table_plies.setColumnWidth(2, 50)
        table_plies.setColumnType(2, AFXTable.INT)
        table_plies.setColumnWidth(3, 80)
        table_plies.setColumnType(3, AFXTable.INT)
        table_plies.setColumnWidth(4, 80)
        table_plies.setColumnType(4, AFXTable.INT)
        # table_plies.setColumnWidth(5, 50)
        # table_plies.setColumnType(5, AFXTable.INT)
        table_plies.setLeadingRowLabels('Layer\tVariables\tLower bound\tUpper bound')
        table_plies.setStretchableColumn(table_plies.getNumColumns() - 1)
        table_plies.showHorizontalGrid(True)
        table_plies.showVerticalGrid(True)
        self.table_plies = table_plies

    def processUpdates(self):

        if self.form.lamina_microscaleKw.getValue() == 1:
            self.GroupBox_3.disable()
            self.GroupBox_2.enable()

        elif self.form.lamina_microscaleKw.getValue() == 2:
            self.GroupBox_2.disable()
            self.GroupBox_3.enable()
            # if self.form.radiusKw.getValue() == 0:
            #     self.GroupBox_6.disable()
            # else:
            #     self.GroupBox_6.enable()

    def onCmdMAT(self, sender, sel, ptr):

        globalVar.add_to_mylaminamat(str(self.form.laminamaterialKw.getValue()))

    def onCmdFiberMAT(self, sender, sel, ptr):

        self.inclusionmat = globalVar.add_to_myinclusionmat(str(self.form.inclusionmaterialKw.getValue()))

    def onCmdMATRIX(self, sender, sel, ptr):
        self.matrixmat = globalVar.add_to_mymatrixmat(str(self.form.matrixmaterialKw.getValue()))

    def onCmdDone(self, sender, sel, ptr):
       

        jobname = globalVar.get_myabq_job()[0]
        with open(jobname) as b:
            lines = b.readlines()

        for i in range(0, len(lines)):
            if lines[i] == "*End Part\n":
                lines.insert(i, "*Include, input=shellsections.inp\n")
                break

        with open(jobname, "w") as b:
            b.writelines(lines)
        b.close()

        def is_num(s):
            try:
                float(s)
            except ValueError:
                return False
            else:
                return True

        
        layup_org = globalVar.get_mylayup()  # "[l1]"

        layup = layup_org.replace("[", "").replace("]", "").split("/")

        for i in range(1, self.tablecoeff.getNumRows()):
            globalVar.add_to_advname(self.tablecoeff.getItemText(i, 1))
            globalVar.add_to_advL(self.tablecoeff.getItemText(i, 2))
            globalVar.add_to_advU(self.tablecoeff.getItemText(i, 3))
            if self.tablecoeff.getItemText(i, 1) != '':
                globalVar.variable_list_bounds(self.tablecoeff.getItemText(i, 1), self.tablecoeff.getItemText(i, 2),
                                           self.tablecoeff.getItemText(i, 3),
                                           self.tablecoeff.getItemText(i, 4))


# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        
        
        # write material properties
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm = mdb.models[modelName].materials
        mat = globalVar.get_mymaterial()[0]
        t = []
        for i in cm[mat].elastic.table:
            for j in range(0, len(i)):
                t.append(i[j])
        
        
        # write arguments in post process part
        args = globalVar.get_myabq_arg()
        f = open(jobname + "args.txt", "w")
        f.write(str(globalVar.get_myabq_name()[0]) + '\n')
        f.write(str(globalVar.get_myabq_script()[0]) + '\n')
        f.write(str(args) + '\n')
        f.write(str(globalVar.get_myabq_step_result()[0]) + '\n')
        f.close()
        
        # write lower, upper bound and partition
        var_dump_coef = []
        for i in range(1, self.tablecoeff.getNumRows()):
            if self.tablecoeff.getItemText(i, 1) != '':
                var_dump_coef.append([self.tablecoeff.getItemText(i, 1),
                                                          self.tablecoeff.getItemText(i, 2),
                                                          self.tablecoeff.getItemText(i, 3), self.tablecoeff.getItemText(i, 4)])

        var_dump_plies = []
        for i in range(1, self.table_plies.getNumRows()):
            if self.table_plies.getItemText(i, 1) != '':
                var_dump_plies.append([self.table_plies.getItemText(i, 1),
                                                          self.table_plies.getItemText(i, 2),
                                                          self.table_plies.getItemText(i, 3), self.table_plies.getItemText(i, 4)])
        
        
                
        f = open(jobname + "LUP.txt", "w")
        f.write(str(var_dump_coef) + '\n')
        f.write(str(var_dump_plies) + '\n')
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
        
        # write number of samples for LHS
        f = open(jobname+"NumofSamples.txt", "w")
        f.write(str(self.form.NumsampleKw.getValue()) + '\n')
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
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML.py abaqus_ps_lhs ' +jobname)
        else:
            os.system('python ' + currentWD + '\\PyYML\\GenerateYML-cyl.py abaqus_ps_lhs ' +jobname)
        
        os.system('datc vs_design_ps_lhs.yml')

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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):
        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.jobnameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, BbDBFileHandler.activate)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):
        fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
                                       self.jobnameKw, self.readOnlyKw,
                                       AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
        fileDb.setReadOnlyPatterns('*.inp')
        fileDb.create()
        fileDb.showModal()
