from abaqusGui import *
from abaqusConstants import ALL
# import osutils, os
import globalVar

###########################################################################
# Class definition
###########################################################################

class ParaDir_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='ParaFunction', objectName='Kernel_Function', registerQuery=False)

        pickedDefault = ''

        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.tablecoeffKw.setColumnType(2, AFXTABLE_TYPE_INT)
        self.tablecoeffKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)

        # if not self.radioButtonGroups.has_key('lamina_option'):
        #     self.lamina_optionKw1 = AFXIntKeyword(None, 'lamina_optionDummy', True)
        #     self.lamina_optionKw2 = AFXStringKeyword(self.cmd, 'lamina_option', True)
        #     self.radioButtonGroups['lamina_option'] = (self.lamina_optionKw1, self.lamina_optionKw2, {})
        # self.radioButtonGroups['lamina_option'][2][528] = 'Lamina '
        # self.lamina_optionKw1.setValue(528)
        # if not self.radioButtonGroups.has_key('microscale_option'):
        #     self.microscale_optionKw1 = AFXIntKeyword(None, 'microscale_optionDummy', True)
        #     self.microscale_optionKw2 = AFXStringKeyword(self.cmd, 'microscale_option', True)
        #     self.radioButtonGroups['microscale_option'] = (self.microscale_optionKw1, self.microscale_optionKw2, {})
        # self.radioButtonGroups['microscale_option'][2][529] = 'Microscale'
        self.lamina_microscaleKw= AFXIntKeyword(self.cmd, 'lamina_microscale', True, 1, evalExpression=False)


        self.laminamaterialKw = AFXStringKeyword(self.cmd, 'laminamaterial', True)
        self.radiusKw = AFXStringKeyword(self.cmd, 'radius', True)
        self.inclusionmaterialKw = AFXStringKeyword(self.cmd, 'inclusionmaterial', True)
        self.inclusion_radiusKw = AFXFloatKeyword(self.cmd, 'inclusion_radius', True)
        self.fiber_radius_tableKw = AFXTableKeyword(self.cmd, 'fiber_radius_table', True)
        self.fiber_radius_tableKw.setColumnType(0, AFXTABLE_TYPE_INT)
        self.fiber_radius_tableKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.fiber_radius_tableKw.setColumnType(2, AFXTABLE_TYPE_INT)
        self.matrixmaterialKw = AFXStringKeyword(self.cmd, 'matrixmaterial', True)
        self.pliesKw = AFXTableKeyword(self.cmd, 'plies', True)
        self.pliesKw.setColumnType(0, AFXTABLE_TYPE_INT)
        self.pliesKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.pliesKw.setColumnType(2, AFXTABLE_TYPE_INT)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import ParaDirDB
        return ParaDirDB.ParaDirDB(self)

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
# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)

globalVar.my_init_para()
globalVar.init_jobname()
globalVar.init_nodeset()
globalVar.init_mylaminamat()
globalVar.init_myinclusionmat()
globalVar.init_mymatrixmat()
globalVar.advpara()
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(buttonText='ATC|4.Parametric study|1.Multi-dimensional sampling',
        object=ParaDir_plugin(toolset),
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        kernelInitString='',
        applicableModules=ALL,
        version='N/A',
        author='N/A',
        description='N/A',
        helpUrl='N/A'
        )
