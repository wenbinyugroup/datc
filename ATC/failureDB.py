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

class FailureDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Failure Criterion',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        self.form = form
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, FailureDB.onCmdDone)

        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_1 = FXGroupBox(p=self, text='Strength', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=5, pb=0)
        l = FXLabel(p=HFrame_1, text='Xt ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_1, ncols=6, labelText='', tgt=form.xtKw, sel=0)
        l = FXLabel(p=HFrame_1, text='Yt', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_1, ncols=6, labelText='', tgt=form.ytKw, sel=0)
        l = FXLabel(p=HFrame_1, text='Zt ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_1, ncols=6, labelText='', tgt=form.ztKw, sel=0)
        HFrame_3 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=20, pb=0)
        l = FXLabel(p=HFrame_3, text='Xc', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_3, ncols=6, labelText='', tgt=form.xcKw, sel=0)
        l = FXLabel(p=HFrame_3, text='Yc', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_3, ncols=6, labelText='', tgt=form.ycKw, sel=0)
        l = FXLabel(p=HFrame_3, text='Zc', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_3, ncols=6, labelText='', tgt=form.zcKw, sel=0)
        HFrame_4 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=20, pb=0)
        l = FXLabel(p=HFrame_4, text='R  ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_4, ncols=6, labelText='', tgt=form.RKw, sel=0)
        l = FXLabel(p=HFrame_4, text='T  ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_4, ncols=6, labelText='', tgt=form.TKw, sel=0)
        l = FXLabel(p=HFrame_4, text='S  ', opts=JUSTIFY_LEFT)
        AFXTextField(p=HFrame_4, ncols=6, labelText='', tgt=form.SKw, sel=0)
        VFrame_1 = FXVerticalFrame(p=self, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=5, pr=0, pt=5, pb=20)
        l = FXLabel(p=VFrame_1, text='Failure Criteria', opts=JUSTIFY_LEFT)
        ComboBox_2 = AFXComboBox(p=VFrame_1, ncols=30, nvis=1, text='', tgt=form.fcriteriaKw, sel=0)
        ComboBox_2.setMaxVisible(10)
        ComboBox_2.appendItem(text='Max-Stress')
        ComboBox_2.appendItem(text='Max-Strain')
        ComboBox_2.appendItem(text='tsai-wu')
        ComboBox_2.appendItem(text='Hashin')
        ComboBox_2.appendItem(text='Tsai-Hill')

    def onCmdDone(self, sender, sel, ptr):
        globalVar.add_to_failure(self.form.fcriteriaKw.getValue())
        S = [self.form.xtKw.getValue(), self.form.ytKw.getValue(), self.form.ztKw.getValue(), self.form.xcKw.getValue(),
             self.form.ycKw.getValue(), self.form.zcKw.getValue(), self.form.RKw.getValue(), self.form.TKw.getValue(),
             self.form.SKw.getValue()]

        for i in S:
            globalVar.add_to_strength(i)
        globalVar.switch_failure1()
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)