from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

import globalVar
from advanceForm import AdvanceForm

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class AdvanceThicknessDB(AFXDataDialog):
    [
        ID_ADVANCE
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST + 1)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        # Construct the base class.
        #
        self.form = form

        AFXDataDialog.__init__(self, form, 'Number of plies', self.OK | self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, AdvanceThicknessDB.onCmdDone)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ADVANCE, AdvanceThicknessDB.onCmdAdvance)

        HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
                                     pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_1, ncols=30, labelText='Equation  ', tgt=form.equationKw, sel=0)

        FXButton(p=HFrame_1, text='From Scripts', tgt=self, sel=self.ID_ADVANCE, opts=BUTTON_NORMAL | LAYOUT_CENTER_Y,
                 x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)
        self.layer_plies_dict = {}

    def onCmdAdvance(self, sender, sel, ptr):
        advanceForm_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        adv = AdvanceForm(advanceForm_new)
        AdvanceForm.activate(adv)

        return 1

    def onCmdDone(self, sender, sel, ptr):
        layer_name = str(self.form.previousParams.get("name"))
        plies_eqn = str(self.form.equationKw.getValue())

        self.layer_plies_dict.update({layer_name: plies_eqn})

        globalVar.add_plies(plies_eqn)
        globalVar.layer_plies(self.layer_plies_dict)

        # add "plies"
        # try:
        #     globalVar.Layer().defineFiberAngles(plies=plies_eqn)
        # except:
        #     globalVar.Layer().addPlies(layer_name=layer_name, plies=plies_eqn)

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
