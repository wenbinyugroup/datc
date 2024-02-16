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

class ParaDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Parametric study from scripts', self.OK | self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place = LAYOUT_SIDE_BOTTOM | LAYOUT_SIDE_RIGHT
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK,ParaDB.onCmdDone)

        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        vf = FXVerticalFrame(VAligner_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 5, 5, 0, 0)

        vf.setSelector(99)
        tablecoeff = AFXTable(vf, 4, 4, 4, 4, form.tablecoeffKw, 4, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        tablecoeff.setLeadingRows(1)
        tablecoeff.setColumnWidth(0, 100)
        tablecoeff.setColumnType(0, AFXTable.TEXT)
        tablecoeff.setColumnType(1, AFXTable.INT)
        tablecoeff.setColumnType(2, AFXTable.INT)
        tablecoeff.setColumnType(3, AFXTable.INT)

        tablecoeff.setLeadingRowLabels('Name \tLower Bound \tUpper Bound \tPartitions ')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff = tablecoeff

    def onCmdDone(self, sender, sel, ptr):

        #
        for i in range(1,self.tablecoeff.getNumRows()):
            globalVar.add_to_advname(self.tablecoeff.getItemText(i,0))
            globalVar.add_to_advL(self.tablecoeff.getItemText(i,1))
            globalVar.add_to_advU(self.tablecoeff.getItemText(i,2))
            globalVar.add_to_advP(self.tablecoeff.getItemText(i,3))

        AFXDataDialog.hide(self)
