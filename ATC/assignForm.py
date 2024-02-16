from abaqusGui import *
from abaqusConstants import ALL
import osutils, os

class AssignForm(AFXForm):
    def __init__(self,owner):
        
        AFXForm.__init__(self,owner)
        self.radioButtonGroups = {}
        self.cmd = AFXGuiCommand(mode=self, method='AssignFunction',objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''

        self.selectedSetKw = AFXStringKeyword(self.cmd, 'selectedSet', True, '')
        
    def getFirstDialog(self):

        import assignDB
        return assignDB.AssignDB(self)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False        