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

class StepsDB(AFXDataDialog):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Steps',
                               self.OK | self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        self.form = form
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, StepsDB.onCmdDone)

        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
                              opts=TABBOOK_NORMAL,
                              x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                              pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='    Abaqus     ', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        VFrame_1 = FXVerticalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
                                   pl=0, pr=0, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=5, pb=5)
        l = FXLabel(p=HFrame_1, text='Name    ', opts=JUSTIFY_LEFT)
        l.setTipText("Step name (arbitrary)")
        AFXTextField(p=HFrame_1, ncols=42, labelText='', tgt=form.name_abqKw, sel=0)

        HFrame_2 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0, pl=5, pr=5, pt=5, pb=5)
        l = FXLabel(p=HFrame_2, text='Jobfile    ', opts=JUSTIFY_LEFT)
        fileHandler = BbDBFileHandler(form, 'jobfile', '*.inp')
        fileTextHf = FXHorizontalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0,
                                       hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=36, labelText='', tgt=form.jobfileKw, sel=0,
                     opts=AFXTEXTFIELD_STRING | LAYOUT_CENTER_Y)
        FXButton(p=fileTextHf, text=' .inp ', tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
                 opts=BUTTON_NORMAL | LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        l.setTipText('Abaqus job file name')

        VAligner_1 = AFXVerticalAligner(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)
        GroupBox_2 = FXGroupBox(p=TabItem_1, text='Post Processsor', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        HFrame_3 = FXHorizontalFrame(p=GroupBox_2, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=10, pb=5)
        l = FXLabel(p=HFrame_3, text='Scripts', opts=JUSTIFY_LEFT)
        l.setTipText('Python script file name for /post-processing ODB')
        AFXTextField(p=HFrame_3, ncols=36, labelText='', tgt=form.scriptKw, sel=0)
        vf = FXVerticalFrame(GroupBox_2, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 8, 2, 2, 2, form.keyword04Kw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 120)
        table.setColumnType(1, AFXTable.FLOAT)
        table.setLeadingRowLabels('Arguments')
        table.setStretchableColumn(table.getNumColumns() - 1)
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        # table.setTipText('Arguments sent to the /post-processing script')
        HFrame_4 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=10, pb=15)
        l = FXLabel(p=HFrame_4, text='Step result file', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_4, ncols=38, labelText='', tgt=form.stepresultKw, sel=0)
        l.setTipText('File name for storing the final output of this step')

        self.tabItem = FXTabItem(p=TabBook_1, text='    Python    ', ic=None, opts=TAB_TOP_NORMAL,
                                 x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_5 = FXHorizontalFrame(p=TabItem_2, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=15, pb=10)
        l = FXLabel(p=HFrame_5, text='Name    ', opts=JUSTIFY_LEFT)
        l.setTipText('Step name (arbitrary)')
        AFXTextField(p=HFrame_5, ncols=40, labelText='', tgt=form.name_pyKw, sel=0)
        HFrame_6 = FXHorizontalFrame(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=5, pb=5)
        l = FXLabel(p=HFrame_6, text='Script     ', opts=JUSTIFY_LEFT)
        l.setTipText('File name of the python script')
        AFXTextField(p=HFrame_6, ncols=40, labelText='', tgt=form.scriptpyKw, sel=0)
        HFrame_7 = FXHorizontalFrame(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=5, pb=5)
        l = FXLabel(p=HFrame_7, text='Function name', opts=JUSTIFY_LEFT)
        l.setTipText('Name of the processing function')
        AFXTextField(p=HFrame_7, ncols=33, labelText=' ', tgt=form.funcnameKw, sel=0)
        HFrame_8 = FXHorizontalFrame(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
                                     pl=5, pr=5, pt=5, pb=5)
        VAligner_2 = AFXVerticalAligner(p=HFrame_8, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=5, pt=5, pb=5)

        GroupBox_2 = FXGroupBox(p=TabItem_2, text='Post Processsor', opts=FRAME_GROOVE | LAYOUT_FILL_X)

        vf = FXVerticalFrame(GroupBox_2, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table1 = AFXTable(vf, 4, 3, 2, 3, form.keyword09Kw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table1.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        table1.setLeadingRows(1)
        table1.setLeadingColumns(1)
        table1.setColumnWidth(1, 80)
        table1.setColumnType(1, AFXTable.TEXT)
        table1.setColumnWidth(2, 200)
        table1.setColumnType(2, AFXTable.FLOAT)
        table1.setLeadingRowLabels('Name\tValue')
        table1.setStretchableColumn(table.getNumColumns() - 1)
        table1.showHorizontalGrid(True)
        table1.showVerticalGrid(True)
        # table1.setTipText('Arguments sent to the processing function')
        self.table = table
        self.table1 = table1

        GroupBox_3 = FXGroupBox(p=TabItem_2, text='Others', opts=FRAME_GROOVE | LAYOUT_FILL_X)

        vf = FXVerticalFrame(GroupBox_3, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table_others = AFXTable(vf, 3, 3, 2, 3, form.othersKw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table_others.setPopupOptions(
            AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW)
        table_others.setLeadingRows(1)
        table_others.setLeadingColumns(1)
        # table_others.setColumnWidth(1, 50)
        # table_others.setColumnType(1, AFXTable.INT)
        # table_others.setColumnWidth(2, 50)
        # table_others.setColumnType(2, AFXTable.INT)
        # table_others.setColumnWidth(3, 80)
        # table_others.setColumnType(3, AFXTable.INT)
        table_others.setLeadingRowLabels('Final\tKeyword')
        table_others.setStretchableColumn(table_others.getNumColumns() - 1)
        table_others.showHorizontalGrid(True)
        table_others.showVerticalGrid(True)
        self.table_others = table_others

    def onCmdDone(self, sender, sel, ptr):
        globalVar.add_to_abq_name(self.form.name_abqKw.getValue())
        globalVar.add_to_abq_job(self.form.jobfileKw.getValue())
        globalVar.add_to_abq_script(self.form.scriptKw.getValue())
        globalVar.add_to_abq_step_result(self.form.stepresultKw.getValue())

        globalVar.add_to_py_name(self.form.name_pyKw.getValue())
        globalVar.add_to_py_script(self.form.scriptpyKw.getValue())
        globalVar.add_to_py_func(self.form.funcnameKw.getValue())

        for i in range(1, self.table.getNumRows()):
            globalVar.add_to_abq_arg(self.table.getItemText(i, 1))

        for i in range(1, self.table1.getNumRows()):
            globalVar.add_to_py_arg_name(self.table1.getItemText(i, 1))
            globalVar.add_to_py_arg_val(self.table1.getItemText(i, 2))

        for i in range(1, self.table_others.getNumRows()):
            if len(self.table_others.getItemText(i, 1)) != 0:
                globalVar.add_to_others(self.table_others.getItemText(i, 1))
                globalVar.add_to_others(self.table_others.getItemText(i, 2))

        # f=open("steps.txt","w")
        # f.write(str("self"))
        # f.close()

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
