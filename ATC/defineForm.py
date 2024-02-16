from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar 

class DefineForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}
        
        self.cmd = AFXGuiCommand(mode=self, method='initValues',objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''
        
        self.viKw = []   
      
        iv =globalVar.get_myinitialvalues()
            
        self.viKw=AFXTupleKeyword(self.cmd,'vi',True,len(iv))

        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.tablecoeffKw.setColumnType(2, AFXTABLE_TYPE_INT)
        self.tablecoeffKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)

        self.pliesKw = AFXTableKeyword(self.cmd, 'plies', True)
        self.pliesKw.setColumnType(0, AFXTABLE_TYPE_INT)
        self.pliesKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.pliesKw.setColumnType(2, AFXTABLE_TYPE_INT)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):
        
        import defineDB
        reload (defineDB)
        return defineDB.DefineDB(self)
        
        

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