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

class AdvanceDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form
        AFXDataDialog.__init__(self, form, 'Define fiber angle from scripts', self.OK | self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place = LAYOUT_SIDE_BOTTOM | LAYOUT_SIDE_RIGHT
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, AdvanceDB.onCmdDone)

        GroupBox_1 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X | LAYOUT_FILL_Y)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        n=55
        l = FXLabel(p=HFrame_1, text='File_name:               ', opts=JUSTIFY_LEFT)
        l.setTipText("filename")
        AFXTextField(p=HFrame_1, ncols=n, labelText='', tgt=form.filenameKw, sel=0)

        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Function_name:', opts=JUSTIFY_LEFT)
        l.setTipText("functionname")
        AFXTextField(p=HFrame_1, ncols=n, labelText='', tgt=form.functionnameKw, sel=0)

        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Transformation:', opts=JUSTIFY_LEFT)
        l.setTipText("transformation")
        AFXTextField(p=HFrame_1, ncols=n, labelText='', tgt=form.transformationKw, sel=0)

        l = FXLabel(GroupBox_1, text='Coefficients:')
        VAligner_2 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=0, pb=0)

        vf = FXVerticalFrame(VAligner_2, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 0, 0, 0, 0)

        vf.setSelector(99)
        tablecoeff = AFXTable(vf, 3, 2, 3, 2, form.tablecoeffKw, 4, AFXTABLE_EDITABLE | LAYOUT_FILL_X )
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS )
        tablecoeff.setLeadingRows(1)
        tablecoeff.setColumnWidth(0, 65)
        tablecoeff.setColumnType(0, AFXTable.TEXT)
        tablecoeff.setColumnWidth(1, 400)
        tablecoeff.setColumnType(1, AFXTable.TEXT)
        tablecoeff.setLeadingRowLabels('Name \tDictionary')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff=tablecoeff
        # VAligner_3 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,pl=0, pr=0, pt=0, pb=0)
        # AFXTextField(p=VAligner_3, ncols=n, labelText='Ply thickness:', tgt=form.thicknessKw, sel=0)
        # AFXTextField(p=VAligner_3, ncols=n, labelText='Number of plies:', tgt=form.pliesKw, sel=0)
        #
        # ComboBox_2 = AFXComboBox(p=VAligner_3, ncols=n-2, nvis=2, text='Material:', tgt=form.matnameKw, sel=0, opts=LAYOUT_FILL_X)
        # ComboBox_2.setMaxVisible(5)
        # vpName = session.currentViewportName
        # modelName = session.sessionState[vpName]['modelName']
        # cm = mdb.models[modelName].materials
        # for i in cm.keys():
        #     ComboBox_2.appendItem(text=i)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,pl=0, pr=0, pt=0, pb=0)

        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=2, pb=0)
        l = FXLabel(p=HFrame_1, text='Multiplier   ', opts=JUSTIFY_LEFT)
        l.setTipText("Multiplier: value shall be 1 or -1 ")
        AFXTextField(p=HFrame_1, ncols=8, labelText='', tgt=form.mKw, sel=0)

    def onCmdDone(self, sender, sel, ptr):
        globalVar.switch1()
        globalVar.flag2()
        globalVar.add_to_choicelist(2)
        globalVar.add_to_mytrans(self.form.transformationKw.getValue())

        coeffname=[]
        coeffval=[]

        for i in range(1,self.tablecoeff.getNumRows()):
            globalVar.add_to_coeffval(self.tablecoeff.getItemText(i, 1))
            coeffval.append(self.tablecoeff.getItemText(i, 1))
            globalVar.add_to_coeffname(self.tablecoeff.getItemText(i, 0))
            coeffname.append(self.tablecoeff.getItemText(i, 0))

        globalVar.add_to_thisdict(self.form.filenameKw.getValue(), self.form.functionnameKw.getValue(),
                                  self.form.transformationKw.getValue(), coeffname, coeffval, self.form.mKw.getValue())
        globalVar.add_to_myfunction(self.form.functionnameKw.getValue())
        globalVar.add_to_myfile(self.form.filenameKw.getValue())
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):

        AFXDataDialog.hide(self)

    def deactivate(self):

        AFXForm.deactivate(self.form)