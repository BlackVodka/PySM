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

"""Functions for generating the state machine's header file.

This module provides functions for generating the state machine's
header file.
Basically, it creates in it's main function the header file itself
and calls subfunctions for generating each needed part of the file.
Only extern needed function should be GenerateHeaderFile().
Subfunctions in this module won't be described, as they just write
file sections and should be self-explaining.
"""

from script import Template_strings as TS
from script import GenHeaderTemplates as GEN
import os
import PySM_Cfg as Cfg
import traceback, time

def GenerateHeaderFile(self, states, config):
    """Generate header file

    This is the main function, generating the state machine's header file.

    Args:
        states: A list of processed state elements. 
        a processed state element is a dict containing
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_entry_instructions" : None or list of entry instruction text lines,
            "list_of_during_instructions" : None or list of during instruction text lines,
            "list_of_exit_instructions" : None or list of exit instruction text lines,
            "is_init_state" : True or False, marking the initial state
        config: A dictionary containing
            'preprocessorInstructions' : A list of preprocessor instruction statement lines,
            'variables' : A list of variable dictionarys, each containing
                'dataType' : A valid datatype as defined in PySM_Cfg.py/list_of_dataTypes,
                'variableName' : The defined variable's name,
                'initialValue' : The initial value of the variable as string
            'inputSignals' : A list of input signal dicts, each containing 
                'dataType': A valid datatype as defined in PySM_Cfg.py/list_of_dataTypes,
                'variableName' : The defined input signal's name,
            'outputSignals' : A list of output signal dicts, each containing,
                'dataType': A valid datatype as defined in PySM_Cfg.py/list_of_dataTypes,
                'variableName' : The defined output signal's name
    """
    hFile = OpenHeaderFile(self)
    if hFile is None:
        return None
    
    # Write file header
    WriteHeaderFileHeader(self, hFile)
    # write preprocessor directives
    WriteHeaderPreprocessorDirectives(self, hFile, config)
    # write typedefs
    WriteHeaderTypedefs(self, hFile, states, config)
    # write APIs
    WriteHeaderApiDeclaration(self, hFile, config)
    # write end of header file
    WriteHeaderEnding(self, hFile)

    
    
    hFile.close()
    #return tuple of header file name and full path, otherwise None will be returned
    fileName = self.txtStateMachineName.text()
    fileName = fileName[0].upper() + fileName[1:] + '.h'
    genResult = (fileName, os.path.realpath(hFile.name))
    return genResult


def OpenHeaderFile(self):
    
    # try opening header file for writing, first character will be uppercase
    hFileName = self.txtStateMachineName.text() + '.h'
    hFileName = hFileName[0].upper() + hFileName[1:]
    filePath = os.path.join(self.txtGenOutputPath.text(), hFileName)
    try:
        hFile = open(filePath, 'w')
    except:
        self.logWindow(TS.LOG_WINDOW_GENERATOR_ERROR_OPENING_OUTPUT_FILE.format( self.txtGenOutputPath.text() + hFileName) )
        traceback.print_exc()
        return None
    
    return hFile


def WriteHeaderFileHeader(self, hFile):
    SM_name = self.txtStateMachineName.text()
    
    try:
        headerTemplate = open(self.txtPathToHeaderTemplate.text(), 'r')
    except:
        headerTemplate = None
        self.logWindow(TS.LOG_WINDOW_GENERATOR_PROBLEM_OPENING_HEADER_TEMPLATE_FILE.format(self.txtPathToHeaderTemplate.text()))
    
    if headerTemplate is not None:
        for line in headerTemplate:
            hFile.write(line)
        headerTemplate.close()
    
    hFile.write(GEN.GENERATED_FILE_DOXYGEN_HEADER.format(
        SM_name[0].upper() + SM_name[1:] + '.h',
        self.txtAuthorName.text(),
        time.strftime("%Y-%m-%d"),
        SM_name,
        time.strftime("%Y-%m-%d"),
        time.strftime("%H:%M:%S")
        ) + '\n')
    
    # write include guard
    hFile.write(GEN.GENERATED_FILE_HEADER_INCLUDE_GUARD.format(
        SM_name.upper(),
        SM_name.upper()
        ) + '\n')
    
    # write includes
    hFile.write(GEN.GENERATED_FILE_HEADER_INCLUDE_HEADING + '\n')
    hFile.write('#include "' + Cfg.lib_typeFileName + '"\n')
    hFile.write('#include "' + Cfg.lib_mainHeaderName + '"\n')
    hFile.write('\n')
        
    return

def WriteHeaderTypedefs(self, hFile, states, config):
    SM_name = self.txtStateMachineName.text()
    
    hFile.write(GEN.GENERATED_FILE_HEADER_TYPEDEFS_HEADING)
    
    # generate input signal typedef
    if config['inputSignals'] is not None:
        hFile.write(GEN.GENERATED_FILE_HEADER_DOXYGEN_INPUT_SIGNALS.format(SM_name))
        hFile.write(GEN.GENERATED_FILE_TYPEDEF_STRUCT_OPENING)
        for inputSignal in config['inputSignals']:
            hFile.write('\t' + inputSignal['dataType'] + ' ' + inputSignal['variableName'] + ';\n')
        hFile.write('} ' + SM_name + '_inputSignalsType' + ';\n\n')
    
    # generate output signal typedef
    if config['outputSignals'] is not None:
        hFile.write(GEN.GENERATED_FILE_HEADER_DOXYGEN_OUTPUT_SIGNALS.format(SM_name))
        hFile.write(GEN.GENERATED_FILE_TYPEDEF_STRUCT_OPENING)
        for outputSignal in config['outputSignals']:
            hFile.write('\t' + outputSignal['dataType'] + ' ' + outputSignal['variableName'] + ';\n')
        hFile.write('} ' + SM_name + '_outputSignalsType' + ';\n\n')
    
    # generate states enum typedef
    hFile.write(GEN.GENERATED_FILE_HEADER_DOXYGEN_STATES.format(SM_name))
    hFile.write(GEN.GENERATED_FILE_TYPEDEF_ENUM_OPENING)
    hFile.write('\t' + SM_name + '_UNINITALIZED_STATE_MACHINE' + ',\n')
    for state in states:
        hFile.write('\t' + SM_name.upper() + '_' + state['state_name'] + ',\n')
    hFile.write('} ' + SM_name + '_activeStateType' + ';\n\n')
    
    return

def WriteHeaderPreprocessorDirectives(self, hFile, config):
    hFile.write(GEN.GENERATED_FILE_HEADER_USER_PREPROCESSOR_DIRECTIVES_HEADING + '\n')
    for preprocessor_line in config['preprocessorInstructions']:
        hFile.write(preprocessor_line + '\n')
    hFile.write('\n')
    
    return

def WriteHeaderApiDeclaration(self, hFile, config):
    SM_name = self.txtStateMachineName.text()
    
    hFile.write(GEN.GENERATED_FILE_HEADER_API_DECLARATION_HEADING)
    hFile.write(GEN.GENERATED_FILE_HEADER_DOXYGEN_MAIN_FUNCTION.format(SM_name) + '\n')
    
    hFile.write(Cfg.lib_returnType + ' ' + SM_name[0].upper() + SM_name[1:] + '_mainFunction(')
    if (config['inputSignals'] is not None) and ((config['outputSignals'] is not None)):
        hFile.write(SM_name + '_inputSignalsType*, ' + SM_name + '_outputSignalsType*' + ');\n\n')
    elif config['inputSignals'] is not None:
        hFile.write(SM_name + '_inputSignalsType*' + ');\n\n')
    elif config['outputSignals'] is not None:
        hFile.write(SM_name + '_outputSignalsType*' + ');\n\n')
    else:
        hFile.write('void' + ');\n\n')
    
    hFile.write(GEN.GENERATED_FILE_HEADER_DOXYGEN_GET_CURRENT_STATE.format(SM_name) + '\n')
    hFile.write('void ' + SM_name[0].upper() + SM_name[1:] + '_getActiveState(' + SM_name + '_activeStateType*' + ');\n\n')

    return

def WriteHeaderEnding(self, hFile):
    SM_name = self.txtStateMachineName.text()
    hFile.write(GEN.GENERATED_FILE_HEADER_ENDING.format(SM_name.upper()))

