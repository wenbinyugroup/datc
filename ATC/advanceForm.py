from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar

###########################################################################
# Class definition
###########################################################################

class AdvanceForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}
        self.cmd = AFXGuiCommand(mode=self, method='', objectName='', registerQuery=False)
        self.filenameKw = AFXStringKeyword(self.cmd, 'filename', True,'users_function')
        self.functionnameKw = AFXStringKeyword(self.cmd, 'functionname', True, 'svFiberAngle')
        self.transformationKw = AFXStringKeyword(self.cmd, 'transformation', True, 'users_function.trans')
        self.thicknessKw = AFXFloatKeyword(self.cmd, 'thickness', True)
        self.pliesKw = AFXIntKeyword(self.cmd, 'plies', True)
        self.matnameKw = AFXStringKeyword(self.cmd, 'matname', True, '')
        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.mKw = AFXStringKeyword(self.cmd, 'm', True) #multiplier

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import advanceDB
        return advanceDB.AdvanceDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
# #
# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)
#
# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
#     buttonText='scripts',
#     object=Scripts_plugin(toolset),
#     messageId=AFXMode.ID_ACTIVATE,
#     icon=None,
#     kernelInitString='',
#     applicableModules=ALL,
#     version='N/A',
#     author='N/A',
#     description='N/A',
#     helpUrl='N/A'
# )

#
# def deactivate(self):
#
#     # self.filenameKw.setValueToPrevious()
#     AFXForm.deactivate(self.form)