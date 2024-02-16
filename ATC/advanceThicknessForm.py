from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
# import globalVar

###########################################################################
# Class definition
###########################################################################

class AdvanceThickness_plugin(AFXForm):
    previousParams = None
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner, myParams):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.previousParams = myParams
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='num_plies',
            objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''
        self.equationKw = AFXStringKeyword(self.cmd, 'equation', True, '')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import advanceThicknessDB
        return advanceThicknessDB.AdvanceThicknessDB(self)

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
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

# globalVar.init_plies()
# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
#     buttonText='AdvanceThickness',
#     object=AdvanceThickness_plugin(toolset),
#     messageId=AFXMode.ID_ACTIVATE,
#     icon=None,
#     kernelInitString='',
#     applicableModules=ALL,
#     version='N/A',
#     author='N/A',
#     description='N/A',
#     helpUrl='N/A'
# )
