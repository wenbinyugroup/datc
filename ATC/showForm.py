from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class ShowForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(self, '','', False)
        self.layupKw = AFXStringKeyword(self.cmd, 'layup', True)

        self.layuptabKw = AFXTableKeyword(self.cmd, 'layuptab', True)
        self.layuptabKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.layuptabKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        pickedDefault = ''

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import showDB
        
        return showDB.ShowDB(self)
        
        

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

# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)

# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
   # buttonText='define', 
   # object=DefineForm(toolset),
   # messageId=AFXMode.ID_ACTIVATE,
   # icon=None,
   # kernelInitString='import Kernel_Function2',
   # applicableModules=ALL,
   # version='N/A',
   # author='N/A',
   # description='N/A',
   # helpUrl='N/A'
# )
