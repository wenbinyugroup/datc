#from abaqusConstants import *
from abaqusGui import *
#from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
thisDir = os.path.join(thisDir, 'Material')


###########################################################################
# Class definition
###########################################################################

class PronyDB(AFXDataDialog):



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Time-dependent Material Data',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        self.form = form
        
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
        
        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
        
        # ======================================================================
        # Upper panel
        GroupBox_1 = FXGroupBox(p=self, text='Method & Analysis', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        
        HFrame_2 = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_2, text='Prony Coefficients', tgt=form.methodKw, sel=1)
        FXRadioButton(p=HFrame_2, text='Time-dependent', tgt=form.methodKw, sel=2)			
        HFrame_3 = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)		
        FXRadioButton(p=HFrame_3, text='Viscoelastic', tgt=form.analysisKw, sel=1)
        FXRadioButton(p=HFrame_3, text='Thermoviscoelastic', tgt=form.analysisKw, sel=2)

        
        # ======================================================================		
        # Lower panel
        HFrame_1 = FXHorizontalFrame(p=self, opts=LAYOUT_FILL_X, 
                                     x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        
        # ----------------------------------------------------------------------
		
        VFrame_2 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
                                   pl=0, pr=0, pt=0, pb=0)
								   
        # ----- Material --------------
        GroupBox_3 = FXGroupBox(p=VFrame_2, text='Material', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        VAligner_3 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)
        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        self.RootComboBox_8 = AFXComboBox(p=VAligner_3, ncols=0, nvis=1, text='Model: ', tgt=form.model_nameKw, sel=0)
        self.RootComboBox_8.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_8.appendItem(name)
        if not form.model_nameKw.getValue() in names:
            form.model_nameKw.setValue( names[0] )
        msgCount = 151
        form.model_nameKw.setTarget(self)
        form.model_nameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler8 = str(self.__class__).split('.')[-1] + '.onComboBox_8MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler8) )


        # Materials combo
        #
        self.ComboBox_8 = AFXComboBox(p=VAligner_3, ncols=0, nvis=1, text='Material: ', tgt=form.Material_matnameKw, sel=0)
        self.ComboBox_8.setMaxVisible(10)

        HFrame_4 = FXHorizontalFrame(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_4, text='Isotropic', tgt=form.AnisotropyKw, sel=1)
        FXRadioButton(p=HFrame_4, text='Engineering constants', tgt=form.AnisotropyKw, sel=2)
        FXRadioButton(p=HFrame_4, text='Orthotropic', tgt=form.AnisotropyKw, sel=3)
        FXRadioButton(p=HFrame_4, text='Anisotropic', tgt=form.AnisotropyKw, sel=4)			
        self.swt_source = FXSwitcher(self, 0, 0,0,0,0, 0,0,0,0)			
		

#--------------------------------------------------------------------------------------------		
#                   Material Input for Isotropic  - Viscoelastic analysis	
#--------------------------------------------------------------------------------------------	
        GroupBox_4 = FXGroupBox(p=self.swt_source, text='Isotropic Material', opts=FRAME_GROOVE)
        VAligner_3 = AFXVerticalAligner(p=GroupBox_4, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)							 
        self.GroupBox_4Note = AFXNote(
            p=GroupBox_4, 
            message='Provide the relaxation times in the first column and Prony coefficient in the following ones.'
           + '\n Note that the same relaxation times should be given for stiffness and CTEs.'
			)
		# Value of relaxed stiffness
        self.E_infinity = AFXTextField(p= VAligner_3 , ncols=16, labelText='E Infinity: ', 
                     tgt=form.E_infinityKw, sel=0)
        # Value of Poisson's ratio
        self.Poisson = AFXTextField(p= VAligner_3  , ncols=16, labelText='Poisson ratio: ', 
                     tgt=form.PoissonKw, sel=0)
				 

        self.verticalf = FXVerticalFrame(VAligner_3, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        self.IsoVisco =AFXTable(self.verticalf, numVisRows=5, numVisColumns=3, numRows=11, numColumns=3,
                     tgt=form.IsoViscoKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.IsoVisco.setLeadingColumns(1)
        self.IsoVisco.setLeadingRows(1)
        self.IsoVisco.setLeadingRowLabels('Lambda_s\tE_s')
        self.IsoVisco.showHorizontalGrid(True)
        self.IsoVisco.showVerticalGrid(True)
        self.IsoVisco.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
		
#--------------------------------------------------------------------------------------------		
#                   Material Input for Isotropic  - Thermoviscoelastic analysis	
#--------------------------------------------------------------------------------------------
        # Value of CTE Infinity					 
        self.CTE = AFXTextField(p= VAligner_3  , ncols=16, labelText='CTE Infinity: ', 
                     tgt=form.CTEKw, sel=0)		
        self.verticalf2 = FXVerticalFrame(VAligner_3, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        # Value of CTE Prony			
        self.IsoViscoCTE =AFXTable(self.verticalf2, numVisRows=5, numVisColumns=3, numRows=11, numColumns=3,
                     tgt=form.IsoViscoCTEKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.IsoViscoCTE.setLeadingColumns(1)
        self.IsoViscoCTE.setLeadingRows(1)
        self.IsoViscoCTE.setLeadingRowLabels('Lambda_s\tCTE_s')
        self.IsoViscoCTE.showHorizontalGrid(True)
        self.IsoViscoCTE.showVerticalGrid(True)
        self.IsoViscoCTE.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		

#--------------------------------------------------------------------------------------------		
#                   Material Input for Engineering Constants  - Viscoelastic analysis	
#--------------------------------------------------------------------------------------------
        GroupBox_5 = FXGroupBox(p=self.swt_source, text='Engineering Constants', opts=FRAME_GROOVE)
        VAligner_4 = AFXVerticalAligner(p=GroupBox_5, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)							 
        self.GroupBox_5Note = AFXNote(
            p=GroupBox_5, 
            message='Provide the relaxation times in the first column and Prony coefficient in the following ones.'
           + '\n Note that the same relaxation times should be given for stiffness and CTEs.'
			)	
		# Value of relaxed stiffness
        self.verticalf3B = FXVerticalFrame(VAligner_4, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)		
        self.EngE_infinity = AFXTable(self.verticalf3B, numVisRows=2, numVisColumns=6, numRows=2, numColumns=10,
                     tgt=form.EngE_infinity, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)	
        self.EngE_infinity.setLeadingColumns(1)
        self.EngE_infinity.setLeadingRows(1)
        self.EngE_infinity.setLeadingRowLabels('E1_Inf\tE2_Inf\tE3_Inf\tNu12_Inf\tNu13_Inf\tNu23_Inf\tG12_Inf\tG13_s\tG23_Inf')
        self.EngE_infinity.showHorizontalGrid(True)
        self.EngE_infinity.showVerticalGrid(True)
        self.EngE_infinity.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		

        self.verticalf3 = FXVerticalFrame(VAligner_4, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        self.EngVisco =AFXTable(self.verticalf3, numVisRows=5, numVisColumns=6, numRows=11, numColumns=11,
                     tgt=form.EngViscoKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.EngVisco.setLeadingColumns(1)
        self.EngVisco.setLeadingRows(1)
        self.EngVisco.setLeadingRowLabels('Lambda_s\tE1_s\tE2_s\tE3_s\tNu12_s\tNu13_s\tNu23_s\tG12_s\tG13_s\tG23_s')
        self.EngVisco.showHorizontalGrid(True)
        self.EngVisco.showVerticalGrid(True)
        self.EngVisco.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
		
		
#--------------------------------------------------------------------------------------------		
#                   Material Input for Engineering Constants - Thermoviscoelastic analysis	
#--------------------------------------------------------------------------------------------
		# Value of CTE Infinity
        self.verticalf3C = FXVerticalFrame(VAligner_4, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)		
        self.EngCTE = AFXTable(self.verticalf3C, numVisRows=2, numVisColumns=4, numRows=2, numColumns=4,
                     tgt=form.EngCTE, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)						 
        self.EngCTE.setLeadingColumns(1)
        self.EngCTE.setLeadingRows(1)
        self.EngCTE.setLeadingRowLabels('CTE11_Inf\tCTE22_Inf\tCTE33_Inf')
        self.EngCTE.showHorizontalGrid(True)
        self.EngCTE.showVerticalGrid(True)
		# Value of CTE Prony		
        self.verticalf4 = FXVerticalFrame(VAligner_4, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)       
        self.EngViscoCTE =AFXTable(self.verticalf4, numVisRows=5, numVisColumns=5, numRows=11, numColumns=5,
                     tgt=form.EngViscoCTEKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.EngViscoCTE.setLeadingColumns(1)
        self.EngViscoCTE.setLeadingRows(1)
        self.EngViscoCTE.setLeadingRowLabels('Lambda_s\tCTE11_s\tCTE22_s\tCTE33_s')
        self.EngViscoCTE.showHorizontalGrid(True)
        self.EngViscoCTE.showVerticalGrid(True)
        self.EngViscoCTE.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
				
#--------------------------------------------------------------------------------------------		
#                   Material Input for Orthotropic  - Viscoelastic analysis	
#--------------------------------------------------------------------------------------------
        GroupBox_6 = FXGroupBox(p=self.swt_source, text='Orthotropic', opts=FRAME_GROOVE)
        VAligner_5 = AFXVerticalAligner(p=GroupBox_6, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)							 
        self.GroupBox_6Note = AFXNote(
            p=GroupBox_6, 
            message='Provide the relaxation times in the first column and Prony coefficient in the following ones.'
           + '\n Note that the same relaxation times should be given for stiffness and CTEs.'
			)	
		# Value of relaxed stiffness
        self.verticalf5B = FXVerticalFrame(VAligner_5, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)			
        self.OrtE_infinity = AFXTable(self.verticalf5B, numVisRows=2, numVisColumns=6, numRows=2, numColumns=10,
                     tgt=form.OrtE_infinity, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)	
        self.OrtE_infinity.setLeadingColumns(1)
        self.OrtE_infinity.setLeadingRows(1)
        self.OrtE_infinity.setLeadingRowLabels('D1111_Inf\tD1122_Inf\tD2222_Inf\tD1133_Inf\tD2233_Inf\tD3333_Inf\tD1212_Inf\tD1313_Inf\tD2323_Inf')
        self.OrtE_infinity.showHorizontalGrid(True)
        self.OrtE_infinity.showVerticalGrid(True)
        self.OrtE_infinity.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
					 
        self.verticalf5 = FXVerticalFrame(VAligner_5, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        self.OrtVisco =AFXTable(self.verticalf5, numVisRows=5, numVisColumns=6, numRows=11, numColumns=11,
                     tgt=form.OrtViscoKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.OrtVisco.setLeadingColumns(1)
        self.OrtVisco.setLeadingRows(1)
        self.OrtVisco.setLeadingRowLabels('Lambda_s\tD1111_s\tD1122_s\tD2222_s\tD1133_s\tD2233_s\tD3333_s\tD1212_s\tD1313_s\tD2323_s')
        self.OrtVisco.showHorizontalGrid(True)
        self.OrtVisco.showVerticalGrid(True)
        self.OrtVisco.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)			
		
#--------------------------------------------------------------------------------------------		
#                   Material Input for Orthotropic - Thermoviscoelastic analysis	
#--------------------------------------------------------------------------------------------
        # Value CTE Infinity
        self.verticalf5C = FXVerticalFrame(VAligner_5, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)		
        self.OrtCTE = AFXTable(self.verticalf5C, numVisRows=2, numVisColumns=4, numRows=2, numColumns=4,
                     tgt=form.OrtCTE, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)						 
        self.OrtCTE.setLeadingColumns(1)
        self.OrtCTE.setLeadingRows(1)
        self.OrtCTE.setLeadingRowLabels('CTE11_Inf\tCTE22_Inf\tCTE33_Inf')
        self.OrtCTE.showHorizontalGrid(True)
        self.OrtCTE.showVerticalGrid(True)
        # Value CTE Prony		
        self.verticalf6 = FXVerticalFrame(VAligner_5, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)       
        self.OrtViscoCTE =AFXTable(self.verticalf6, numVisRows=5, numVisColumns=5, numRows=11, numColumns=5,
                     tgt=form.OrtViscoCTEKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0,
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)						 
        self.OrtViscoCTE.setLeadingColumns(1)
        self.OrtViscoCTE.setLeadingRows(1)
        self.OrtViscoCTE.setLeadingRowLabels('Lambda_s\tCTE11_s\tCTE22_s\tCTE33_s')
        self.OrtViscoCTE.showHorizontalGrid(True)
        self.OrtViscoCTE.showVerticalGrid(True)
        self.OrtViscoCTE.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
				
#--------------------------------------------------------------------------------------------		
#                   Material Input for Anisotropic  - Viscoelastic analysis	
#--------------------------------------------------------------------------------------------
        GroupBox_7 = FXGroupBox(p=self.swt_source, text='Anisotropic', opts=FRAME_GROOVE)
        VAligner_6 = AFXVerticalAligner(p=GroupBox_7, opts=0, x=0, y=0, w=0, h=0,
                                        pl=0, pr=0, pt=0, pb=0)							 
        self.GroupBox_7Note = AFXNote(
            p=GroupBox_7, 
            message='Provide the relaxation times in the first column and Prony coefficient in the following ones.'
           + '\n Note that the same relaxation times should be given for stiffness and CTEs.'
			)	
		# Value of relaxed stiffness
        self.verticalf7B = FXVerticalFrame(VAligner_6, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        self.AniE_infinity = AFXTable(self.verticalf7B, numVisRows=2, numVisColumns=6, numRows=2, numColumns=22,
                     tgt=form.AniE_infinity, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)
        self.AniE_infinity.setLeadingColumns(1)
        self.AniE_infinity.setLeadingRows(1)
        self.AniE_infinity.setLeadingRowLabels('D1111_Inf\tD1122_Inf\tD2222_Inf\tD1133_Inf\tD2233_Inf\tD3333_Inf\tD1112_Inf\tD2212_Inf\tD3312_Inf\tD1212_Inf\tD1113_Inf\tD2213_Inf\tD3313_Inf\tD1213_Inf\tD1313_Inf\tD1123_Inf\tD2223_Inf\tD3323_Inf\tD1223_Inf\tD1323_Inf\tD2323_Inf')
        self.AniE_infinity.showHorizontalGrid(True)
        self.AniE_infinity.showVerticalGrid(True)
        self.AniE_infinity.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		

        self.verticalf7 = FXVerticalFrame(VAligner_6, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)
        self.AniVisco =AFXTable(self.verticalf7, numVisRows=5, numVisColumns=6, numRows=11, numColumns=23,
                     tgt=form.AniViscoKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)					 
        self.AniVisco.setLeadingColumns(1)
        self.AniVisco.setLeadingRows(1)
        self.AniVisco.setLeadingRowLabels('Lambda_s\tD1111_s\tD1122_s\tD2222_s\tD1133_s\tD2233_s\tD3333_s\tD1112_s\tD2212_s\tD3312_s\tD1212_s\tD1113_s\tD2213_s\tD3313_s\tD1213_s\tD1313_s\tD1123_s\tD2223_s\tD3323_s\tD1223_s\tD1323_s\tD2323_s')
        self.AniVisco.showHorizontalGrid(True)
        self.AniVisco.showVerticalGrid(True)
        self.AniVisco.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)				
		
#--------------------------------------------------------------------------------------------		
#                   Material Input for Anisotropic - Thermoviscoelastic analysis	
#--------------------------------------------------------------------------------------------
        # Value of CTE Infinity
        self.verticalf7C = FXVerticalFrame(VAligner_6, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)		
        self.AniCTE = AFXTable(self.verticalf7C, numVisRows=2, numVisColumns=6, numRows=2, numColumns=7,
                     tgt=form.AniCTE, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0, 
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)
        self.AniCTE.setLeadingColumns(1)
        self.AniCTE.setLeadingRows(1)
        self.AniCTE.setLeadingRowLabels('CTE11_Inf\tCTE22_Inf\tCTE33_Inf\tCTE12_Inf\tCTE13_Inf\tCTE23_Inf')
        self.AniCTE.showHorizontalGrid(True)
        self.AniCTE.showVerticalGrid(True)	
        # Value of CTE Prony	
        self.verticalf8 = FXVerticalFrame(VAligner_6, FRAME_SUNKEN|FRAME_THICK, 0,0,0,0,0,0,0,0)       
        self.AniViscoCTE =AFXTable(self.verticalf8, numVisRows=5, numVisColumns=6, numRows=11, numColumns=8,
                     tgt=form.AniViscoCTEKw, sel=0, opts=AFXTABLE_EDITABLE, x=0, y=0, w=0, h=0,
                     pl= DEFAULT_MARGIN, pr=DEFAULT_MARGIN, pt=DEFAULT_MARGIN, pb=DEFAULT_MARGIN)						 
        self.AniViscoCTE.setLeadingColumns(1)
        self.AniViscoCTE.setLeadingRows(1)
        self.AniViscoCTE.setLeadingRowLabels('Lambda_s\tCTE11_s\tCTE22_s\tCTE33_s\tCTE12_s\tCTE13_s\tCTE23_s')
        self.AniViscoCTE.showHorizontalGrid(True)
        self.AniViscoCTE.showVerticalGrid(True)
        self.AniViscoCTE.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_CUT|AFXTable.POPUP_PASTE)		
				


#--------------------------------------------------------------------------------------------		
#                   Material Input for Time-Dependent data
#--------------------------------------------------------------------------------------------
 		
        GroupBox_8 = FXGroupBox(p=self.swt_source, text='Material from file', opts=FRAME_GROOVE|LAYOUT_FILL_X)   	   
        HFrame_8 = FXHorizontalFrame(p=GroupBox_8, opts=LAYOUT_FILL_X, 
                                    x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        
        # ----------------------------------------------------------------------
        VFrame_8 = FXVerticalFrame(p=HFrame_8, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)

        fileHandler = MaterialData_FileHandler(form, 'file_material_input', 'All files (*)')
        fileTextHf = FXHorizontalFrame(p=VFrame_8, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=32, labelText='Material data file: ', tgt=form.file_material_inputKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='\tSelect File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
     
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.model_nameKw.setValue(self.currentModelName)
        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_8Materials)
        self.CTE.disable()
        self.IsoViscoCTE.disable()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_8Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_8MaterialsChanged(self, sender, sel, ptr):

        self.updateComboBox_8Materials()
        return 1

      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_8Materials(self):

        modelName = self.form.model_nameKw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_8.clearItems()
        names = mdb.models[modelName].materials.keys()
        names.sort()
        for name in names:
            self.ComboBox_8.appendItem(name)
        if names:
            if not self.form.Material_matnameKw.getValue() in names:
                self.form.Material_matnameKw.setValue( names[0] )
        else:
            self.form.Material_matnameKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def processUpdates(self):
        
        if self.form.methodKw.getValue() == 1:
            if self.form.AnisotropyKw.getValue() == 1:
				self.swt_source.setCurrent(0)			
				if self.form.analysisKw.getValue() == 1:
					self.IsoVisco.enable()
					self.CTE.disable()
					self.IsoViscoCTE.disable()					
				elif self.form.analysisKw.getValue() == 2:
					self.CTE.enable()
					self.IsoViscoCTE.enable()
            elif self.form.AnisotropyKw.getValue() == 2:
				self.swt_source.setCurrent(1)			
				if self.form.analysisKw.getValue() == 1:
					self.EngVisco.enable()
					self.EngCTE.disable()
					self.EngViscoCTE.disable()					
				elif self.form.analysisKw.getValue() == 2:
					self.EngCTE.enable()
					self.EngViscoCTE.enable()
            elif self.form.AnisotropyKw.getValue() == 3:
				self.swt_source.setCurrent(2)			
				if self.form.analysisKw.getValue() == 1:
					self.OrtVisco.enable()
					self.OrtCTE.disable()
					self.OrtViscoCTE.disable()					
				elif self.form.analysisKw.getValue() == 2:
					self.OrtCTE.enable()
					self.OrtViscoCTE.enable()
            elif self.form.AnisotropyKw.getValue() == 4:
				self.swt_source.setCurrent(3)			
				if self.form.analysisKw.getValue() == 1:
					self.AniVisco.enable()
					self.AniCTE.disable()
					self.AniViscoCTE.disable()					
				elif self.form.analysisKw.getValue() == 2:
					self.AniCTE.enable()
					self.AniViscoCTE.enable()					
				
        elif self.form.methodKw.getValue() == 2:
            self.swt_source.setCurrent(4)


###########################################################################
# Class definition
###########################################################################

class MaterialData_FileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, MaterialData_FileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()