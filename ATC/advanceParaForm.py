from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar

###########################################################################
# Class definition
###########################################################################

class AdvanceParaForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='', objectName='', registerQuery=False)
        pickedDefault = ''
        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import advanceParaDB
        return advanceParaDB.ParaDB(self)

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

    # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

globalVar.advpara()
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Register the plug-in
# #
# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)
#
# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
#     buttonText='para',
#     object=Para_plugin(toolset),
#     messageId=AFXMode.ID_ACTIVATE,
#     icon=None,
#     kernelInitString='',
#     applicableModules=ALL,
#     version='N/A',
#     author='N/A',
#     description='N/A',
#     helpUrl='N/A'
# )
