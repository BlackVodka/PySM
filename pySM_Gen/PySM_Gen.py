##############################################################################
# Copyright (C) 2017 by Markus Burger                                        #
#                                                                            #
# This file is part of pySM - The python state machine code generator        #
#                                                                            #
#   pySM is free software: you can redistribute it and/or modify it          #
#   under the terms of the GNU Lesser General Public License as published    #
#   by the Free Software Foundation, either version 3 of the License, or     #
#   (at your option) any later version.                                      #
#                                                                            #
#   PySM is distributed in the hope that it will be useful,                  #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Lesser General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Lesser General Public         #
#   License along with Box.  If not, see <http://www.gnu.org/licenses/>.     #
##############################################################################

"""PySM Generator module

This is the PySM main module.
It creates the main GUI, starts and handles the subroutines for
parsing the yEd *graphml - files, processing this results and
generating the according *.c and *.h files for the given
state machine.
"""

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
from ui.PySM_ui import Ui_PySm_MainWindow
import PySM_Cfg as Cfg
from script import Template_strings as TS
from script.GraphmlParser import ParseGraphmlFile
from script.ProcessStateText import ProcessStateText
from script.ProcessTransitionText import ProcessTransitionText
from script.ProcessConfigurationText import ProcessConfigurationText
from script.PatchIOSignalNames import Patch_states, Patch_transitions
from script.GenerateHeaderFile import GenerateHeaderFile
from script.GenerateSourceFile import GenerateSourceFile
from pprint import pprint
import time, traceback

__ENABLE_DEBUG__ = True

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class PySM_Gen_MainWindowClass(Ui_PySm_MainWindow):
    """PySM main window class

    This class creates based on the Qt Designer created GUI
    class Ui_PySm_MainWindow a subclass.
    It connects the Qt events to the according slots and
    provides some methods explained in detail in
    the according method's implementation.
    """
    def __init__(self, mainWindow):
        """Connects the Qt signals to the according slot methods,
        tries to create a logfile.

    Connects the used Qt signals to the according slots
    (= class methods).
    Also, tries to create a logfile and informs the rest of the program
    by setting self.logging_to_file_enabled if the logfile's creation
    was successful or not.
    """
        Ui_PySm_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        
        self.logging_to_file_enabled = False
        self.nOfWarnings = 0
        self.nOfErrors = 0
        
        # Connect buttons to according functions
        self.btnGenerate.clicked.connect(self.startGeneration)
        self.btnSelectHeaderFile.clicked.connect(self.browseForHeaderFile)
        self.btnSelectyEDInputFile.clicked.connect(self.browseForyEDInputFile)
        self.btnSelectOutputPath.clicked.connect(self.browseForOutputDirectory)
        
        # Connect text fields for enabling drag/drop support
        self.txtPathToyEDInputFile.textChanged.connect(self.inputFilePathChanged)
        self.txtPathToHeaderTemplate.textChanged.connect(self.headerFilePathChanged)
        self.txtGenOutputPath.textChanged.connect(self.outputPathChanged)
        
        try:
            self.logfile = open(Cfg.logfile_name, 'w')
        except:
            self.logWindow(TS.LOG_WINDOW_ERROR_OPENING_LOGFILE.format(Cfg.logfile_name))
            traceback.print_exc()
        else:
            self.logging_to_file_enabled = True
            self.logfile.write( ('Started logging {}\n').format(time.strftime("%c")) )
            self.logfile.close()
        self.txtGenOutputPath.setText(Cfg.default_output_path)


    
    def browseForHeaderFile(self):
        """Opens a 'File Open' dialog for browsing for a
        code header template file.

    Tries to use the entered path as starting point, if given.
    Else, it uses the generator module's file path as start.
    Opens a file open dialog for browsing for a code header template file.
    """
        (inPath, _inFile) = os.path.split(self.txtPathToHeaderTemplate.text())
        if not os.path.isdir(inPath):
            # use current dir as start dir
            inPath = os.getcwd()
        inFilePath = self.getfile("Header templates (*.txt)", inPath)
        if not inFilePath == '':
            self.txtPathToHeaderTemplate.setText(inFilePath)
        
    def browseForyEDInputFile(self):
        """Opens a 'File Open' dialog for browsing for a
        yEd graphml file.

    Tries to use the entered path as starting point, if given.
    Else, it uses the generator module's file path as start.
    Opens a file open dialog for browsing for a yEd graphml file.
    """
        (inPath, _inFile) = os.path.split(self.txtPathToyEDInputFile.text())
        if not os.path.isdir(inPath):
            # use current dir as start dir
            inPath = os.getcwd()
        inFilePath = self.getfile("yED graph files (*.graphml)", inPath)
        if not inFilePath == '':
            self.txtPathToyEDInputFile.setText(inFilePath)

    def browseForOutputDirectory(self):
        """Opens a 'File Open' dialog for browsing for a
        code generation output directory.

    Tries to use the entered path as starting point, if given.
    Else, it uses the generator module's file path as start.
    Opens a file open dialog for browsing for a code generation output dir.
    """
        outPath = self.txtGenOutputPath.text()
        if not os.path.isdir(outPath):
            # use current dir as start dir
            outPath = os.getcwd()
        outDir = str(QFileDialog.getExistingDirectory(None, "Select Directory", outPath))
        if not outDir == '':
            self.txtGenOutputPath.setText(outDir)
        
    def startGeneration(self):
        """Code generation function.

    Handles the whole generation process.
    Calls the needed submodules and handles exceptions.
    Also, outputs debug information to GUI's log window.
    """
        self.txtGenerationOutput.clear()
        self.logWindow(TS.LOG_WINDOW_GENERATION_STARTED)
        if self.checkInputs() == False:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        
        ######################
        # Parse graphml file #
        ######################
        try:
            (parsedStates, parsedConfig, parsedTransitions) = ParseGraphmlFile(self)
        except:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            traceback.print_exc()
            return
        self.logWindow(TS.LOG_WINDOW_FINISHED_PARSING.format(len(parsedStates), len(parsedConfig), len(parsedTransitions)))
        self.logWindow(TS.LOG_WINDOW_STATE_TEXT_PROCESSING_IN_PROGRESS)
        if __ENABLE_DEBUG__:
            self.debugLog(dbg_parsedStates = parsedStates, dbg_parsedConfig = parsedConfig, dbg_parsedTransitions = parsedTransitions)

        #######################
        # Process state texts #
        #######################
        try:
            (processedStates, ProcessedStateStats) = ProcessStateText(self, parsedStates)
        except:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            traceback.print_exc()
            return
        
        if processedStates is None:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        self.logWindow(TS.LOG_WINDOW_FINISHED_STATE_TEXT_PROCESSING.format(
            ProcessedStateStats["nOfEntries"], ProcessedStateStats["nOfDurings"], ProcessedStateStats["nOfExits"]) )
        if __ENABLE_DEBUG__:
            self.debugLog(dbg_processedStates = processedStates)
        
        ############################
        # Process transition texts #
        ############################
        self.logWindow(TS.LOG_WINDOW_TRANSITION_TEXT_PROCESSING_IN_PROGRESS)
        try:
            (processedTransitions, ProcessedTransitionStats) = ProcessTransitionText(self, parsedTransitions)
        except:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            traceback.print_exc()
            return
        
        if processedTransitions is None:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        self.logWindow(TS.LOG_WINDOW_FINISHED_TRANSITION_TEXT_PROCESSING.format(
            ProcessedTransitionStats["nOfConditions"], ProcessedTransitionStats["nOfActions"], ProcessedTransitionStats["nOfBlanks"]) )
        if __ENABLE_DEBUG__:
            self.debugLog(dbg_processedTransitions = processedTransitions)
        
        ###############################
        # Process configuration texts #
        ###############################
        self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IN_PROGRESS)
        try:
            (processedConfigurations, ProcessedConfigurationStats) = ProcessConfigurationText(self, parsedConfig)
        except:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            traceback.print_exc()
            return
        
        if processedConfigurations is None:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        self.logWindow(TS.LOG_WINDOW_FINISHED_CONFIGURATION_TEXT_PROCESSING.format(
            ProcessedConfigurationStats["nOfInputSignals"],
            ProcessedConfigurationStats["nOfOutputSignals"],
            ProcessedConfigurationStats["nOfVariables"],
            ProcessedConfigurationStats["nOfPreprocessorLines"]) )
        if __ENABLE_DEBUG__:
            self.debugLog(dbg_processedConfigurations = processedConfigurations)
        
        #####################################################################################################
        # Patch occurences of in- and output signals in transition conditions, actions and in state actions #
        #####################################################################################################
        if not((ProcessedConfigurationStats["nOfInputSignals"] == 0) and (ProcessedConfigurationStats["nOfOutputSignals"] == 0)):
            self.logWindow(TS.LOG_WINDOW_PATCH_STATE_TEXT_IN_PROGRESS)
            (nOfPatchedStates,nOfPatchedElems) = Patch_states(self, processedStates, processedConfigurations)
            self.logWindow(TS.LOG_WINDOW_PATCH_STATE_TEXT_FINISHED.format(nOfPatchedStates, nOfPatchedElems))
            self.logWindow(TS.LOG_WINDOW_PATCH_TRANSITION_TEXT_IN_PROGRESS)
            (nOfPatchedTransitions,nOfPatchedElems) = Patch_transitions(self, processedTransitions, processedConfigurations)
            self.logWindow(TS.LOG_WINDOW_PATCH_TRANSITION_TEXT_FINISHED.format(nOfPatchedTransitions, nOfPatchedElems))
            if __ENABLE_DEBUG__:
                self.debugLog(dbg_patchedStates = processedStates, dbg_patchedTransitions = processedTransitions)
        
        #########################
        # Start code generation #
        #########################
        self.logWindow(TS.LOG_WINDOW_INVOKING_GENERATOR)
        (hFileName, hFullPath) = GenerateHeaderFile(self, processedStates, processedConfigurations)
        if hFileName is None:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        
        (cFileName, cFullPath) = GenerateSourceFile(self, processedStates, processedTransitions, processedConfigurations)
        if cFileName is None:
            self.logWindow(TS.LOG_WINDOW_GENERATION_ERROR)
            return
        
        self.logWindow(TS.LOG_WINDOW_GENERATION_FINISHED)
        self.logWindow(TS.LOG_WINDOW_GENERATION_STATS.format(hFileName, hFullPath, cFileName, cFullPath, self.nOfWarnings, self.nOfErrors) )
        
        # Function for appending text to log window without automatic newline
    def logWindow(self, *args):
        """Function for appending text to the GUIs log output.

    Appends text to the GUIs log output without an implicit newline.
    Also, colors the text based on the text's tags.
    Outputted text is also written to the generator logfile.
    """
        self.txtGenerationOutput.moveCursor(QtGui.QTextCursor.End)
        cursor = self.txtGenerationOutput.textCursor()
        txtFormat = QtGui.QTextCharFormat()
        
        if self.logging_to_file_enabled:
                self.logfile = open(Cfg.logfile_name, 'a')
        
        for txt in args:
            if "[Error]" in txt.split():
                self.nOfErrors += 1
                txtFormat.setFontWeight( QtGui.QFont.Bold );
                txtFormat.setForeground(QtGui.QBrush(QtGui.QColor( "red" )))
            elif "[Warning]" in txt.split():
                self.nOfWarnings += 1
                txtFormat.setFontWeight( QtGui.QFont.Bold );
                txtFormat.setForeground(QtGui.QBrush(QtGui.QColor( "blue" )))
            else:
                txtFormat.setFontWeight( QtGui.QFont.Normal );
                txtFormat.setForeground(QtGui.QBrush(QtGui.QColor( "black" )))
            cursor.setCharFormat(txtFormat)
            cursor.insertText(txt)
            if self.logging_to_file_enabled:
                self.logfile.write(txt)
                
        self.txtGenerationOutput.moveCursor(QtGui.QTextCursor.End)
        self.logfile.close()
   
        
    def debugLog(self, **kwargs):
        """Prints debugging information to generator logfile.

    Prints debugging information to generator logfile, if called.
    """
        if self.logging_to_file_enabled:
            self.logfile = open(Cfg.logfile_name, 'a')
            self.logfile.write(TS.DEBUG_HEADER_START)
            for name, elem in kwargs.items():
                print(name, '\n', file=self.logfile)
                pprint(elem, stream=self.logfile)
                print('\n\n', file=self.logfile)
                
            self.logfile.write(TS.DEBUG_HEADER_STOP)
            self.logfile.close()
        
        # Open file dialog
    def getfile(self, fileFilter, startPath):
        fname, _filter = QFileDialog.getOpenFileName(None, "Open file", startPath, fileFilter)
        return fname
    
    def inputFilePathChanged(self):
        """Handle changed text of yEd input file path.

    Removes preceeding file:// tag, if a file is given by drag & drop.
    """
        # Remove file:// string, if existing
        yedPath = self.txtPathToyEDInputFile.text()
        if 'file://' in yedPath:
            yedPath = yedPath.replace("file://", "")
            self.txtPathToyEDInputFile.setText(yedPath)
            
    def headerFilePathChanged(self):
        """Handle changed text of code header template file path.

    Removes preceeding file:// tag, if a file is given by drag & drop.
    """
        # Remove file:// string, if existing
        headerPath = self.txtPathToHeaderTemplate.text()
        if 'file://' in headerPath:
            headerPath = headerPath.replace("file://", "")
            self.txtPathToHeaderTemplate.setText(headerPath)
            
    def outputPathChanged(self):
        """Handle changed text of output dir path.

    Removes preceeding file:// tag, if a output filder is given by drag & drop.
    """
        # Remove file:// string, if existing
        outPath = self.txtGenOutputPath.text()
        if 'file://' in outPath:
            outPath = outPath.replace("file://", "")
            self.txtGenOutputPath.setText(outPath)
    
    def checkInputs(self):
        """Do some trivial checks for given inputs

    Does some basic sanity check for the given inputs by checking if
    any input given (elsewise, either set a default or raise an error
    with an log window output)
    """
        InTxt = self.txtPathToyEDInputFile.text()
        if len(InTxt) == 0:
            self.logWindow(TS.LOG_WINDOW_NO_YED_INPUT_FILE_GIVEN)
            return False
        InTxt = self.txtStateMachineName.text()
        if len(InTxt) == 0:
            self.logWindow(TS.LOG_WINDOW_NO_STATEMACHINE_NAME_GIVEN)
            return False
        InTxt = self.txtPathToHeaderTemplate.text()
        if len(InTxt) == 0:
            self.txtPathToHeaderTemplate.setText(Cfg.default_code_header_file)
            self.logWindow(TS.LOG_WINDOW_USING_DEFAULT_HEADER_FILE, Cfg.default_code_header_file,'\n')
        InTxt = self.txtAuthorName.text()
        if len(InTxt) == 0:
            self.txtAuthorName.setText(Cfg.default_author_name)
            self.logWindow(TS.LOG_WINDOW_USING_DEFAULT_AUTHOR_NAME, Cfg.default_author_name,'\n')
        InTxt = self.txtGenOutputPath.text()
        if len(InTxt) == 0:
            self.txtGenOutputPath.setText(Cfg.default_output_path)
            self.logWindow(TS.LOG_WINDOW_USING_DEFAULT_OUTPUT_DIR, Cfg.default_output_path,'\n')
            


if __name__ == '__main__':
    """Code generator's main function.

    Changes the pyQt5's except hook to the classical one for
    changing exception behaviour (printing a traceback to console instead
    of just aborting execution).
    Also, creates the GUI's class and activates it by calling it's show method.
    """
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = QMainWindow()
    PySM_MainWindowInstance = PySM_Gen_MainWindowClass(window)
    window.setWindowIcon(QtGui.QIcon("ui/icon.png"))
    window.show()
    sys.exit(app.exec_())
