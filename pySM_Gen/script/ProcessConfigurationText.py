##############################################################################
# Copyright (C) 2017 by Markus Burger                                        #
#                                                                            #
#   This file is part of pySM - The python state machine code generator      #
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

"""Functions for processing configuration texts

This module provides functions for processing configuration texts,
e.g. finding preprocessor, variables, in-and output signal statements.
Only extern needed function should be ProcessConfigurationText()
"""

from script import Template_strings as TS
import PySM_Cfg as Cfg


def ProcessConfigurationText(self, parsedConfig):
    """Process configuration texts

    For easier use of the configuration objects, the raw parsed
    configurations are processed and split into their containing
    informations, described in the return section below.
    For the variable, in- and output signals some basic checks
    like searching for a ';', checking the given file type etc.
    are also implemented.

    Args:
        parsedConfig: A parsed configuration dictionary, containing
            "cfgVarLines": None or text of a cfgKw_variables configuration block,
            "cfgPreprocessorLines" : None or text of a cfgKw_defines config block,
            "cfgInSigLines" : None or text of a cfgKw_inSigs config block,
            "cfgOutSigLines" : None or text of a cfgKw_outSigs config block

    Returns:
        None, if a error happened or
        A dictionary containing
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
    
    processedConfig = {
        'preprocessorInstructions' : None,
        'variables' : None,
        'inputSignals' : None,
        'outputSignals' : None
        }
    
    stats = {
        'nOfInputSignals' : None,
        'nOfOutputSignals' : None,
        'nOfVariables' : None,
        'nOfPreprocessorLines' : None
        }
    
    ####################################################################################
    # preprocessor instructions can't really be checked for validity, copying 'em over #
    ####################################################################################
    if parsedConfig['cfgPreprocessorLines'] is not None:
        processedConfig['preprocessorInstructions'] = parsedConfig['cfgPreprocessorLines']
        stats['nOfPreprocessorLines'] = len(processedConfig['preprocessorInstructions'])
    
    ##################################
    # process in- and output signals #
    ##################################
    if parsedConfig['cfgInSigLines'] is not None:
        processedConfig['inputSignals'] = Process_IO_signals(self, parsedConfig['cfgInSigLines'])
        if processedConfig['inputSignals'] is not None:
            stats['nOfInputSignals'] = len(processedConfig['inputSignals'])
    if parsedConfig['cfgOutSigLines'] is not None:
        processedConfig['outputSignals'] = Process_IO_signals(self, parsedConfig['cfgOutSigLines'])
        if processedConfig['outputSignals'] is not None:
            stats['nOfOutputSignals'] = len(processedConfig['outputSignals'])
                
    #####################
    # process variables #
    #####################
    if parsedConfig['cfgVarLines'] is not None:
        processedConfig['variables'] = Process_variables(self, parsedConfig['cfgVarLines'])
        if processedConfig['variables'] is not None:
            stats['nOfVariables'] = len(processedConfig['variables'])

    return(processedConfig, stats)


def Process_IO_signals(self, config):
    """Process configuration in-/output signals

    Searches for valid in-/output signals

    Args:
        config: A list of either input or output signal configuration lines

    Returns:
        None, if an error happened/no valid I/O-signals were found
        or a list of processed element dicts, containing
            'dataType': A valid datatype as defined in PySM_Cfg.py/list_of_dataTypes,
            'variableName' : The processed signal's name
    """
    listOfProcessedElements = []
    for ioLine in config:
            
        splittedLine = ioLine.split(' ')
        # first part of variables should be a valid data type and a variable name should follow up
        if Cfg.__ENABLE_VARIABLE_TYPECHECK__:
            if not(splittedLine[0] in Cfg.list_of_dataTypes) or not(len(splittedLine) == 2):
                self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IO_PROBLEM.format(ioLine))
                continue #with next line
        else:
                if not(len(splittedLine) == 2):
                    self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IO_PROBLEM.format(ioLine))
                    continue #with next line

        # last symbol should be a semicolon
        if ioLine.rfind(';') == -1:
            self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IO_PROBLEM.format(ioLine))
            continue
        
        # remove semicolon from var Name
        splittedLine[1] = (splittedLine[1])[:-1]

        elem = {
            'dataType': splittedLine[0],
            'variableName' : splittedLine[1]
            }
        listOfProcessedElements.append(elem)
    
    if not( len(listOfProcessedElements) == 0):
        return listOfProcessedElements
    else:
        return None

    
def Process_variables(self, configTxt):
    """Process configuration variable texts

    Searches for valid variable definitions

    Args:
        configTxt: A list of configuration variable definition lines

    Returns:
        None, if an error happened/no valid variables were found
        or a list of processed variable dicts, containing
            'preceedingKeyWord' : A valid preceeding keyword like const or volatile
            'dataType' : A valid datatype as defined in PySM_Cfg.py/list_of_dataTypes,
            'variableName' : The processed signal's name,
            'initialValue' : The initial value of the variable as string
    """
    
    listOfVariables = []
    
    for varLine in configTxt:
        elem = {
        'preceedingKeyWord' : None,
        'dataType' : None,
        'variableName' : None,
        'initialValue' : None
        }
        # at least one equal sign should be there to assign an initial value
        splittedLine = varLine.split('=')
        if len(splittedLine) > 2:
            self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_TO_MUCH_EQUAL_SIGNS.format(varLine))
            continue #with next line
        # we have ony one equal sign, now we search for correct separated variable name and initial value
        splittedLine = varLine.split(' = ')
        if splittedLine[-1].rfind(';') == -1:
            self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_NO_SEMICOLON.format(varLine))
            continue #with next line
        elif len(splittedLine) == 1:
            self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_NO_INIT_VALUE.format(varLine))
            elem['initialValue'] = '0'
        # at this point, the line contains one '=' sign and ends with a ';', continue with processing
        else:
            initialValue = splittedLine[-1]
            # remove ';'
            elem['initialValue'] = initialValue[0:-1]

        # continue with finding variable type and name
        firstLinePart = (splittedLine[0]).split(' ')
        if not (len(firstLinePart) == 2):
            # Found an additional preceeeding variable codeword?
            if (len(firstLinePart) == 3):
                # Is preceeding variable word a valid codeword?
                if (firstLinePart[0] in Cfg.list_ofPreceedingVariableKeywords):
                    # everything ok
                    pass
                else:
                    self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_INVALID_VARIABLE_NAME_OR_DATATYPE.format(varLine))
                    continue #with next line
            else:
                self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_INVALID_VARIABLE_NAME_OR_DATATYPE.format(varLine))
                continue #with next line
        
        if (len(firstLinePart) == 3):
            varType = firstLinePart[1]
            elem['preceedingKeyWord'] = firstLinePart[0]
            elem['variableName'] = firstLinePart[2]
        else:
            varType = firstLinePart[0]
            elem['variableName'] = firstLinePart[1]
        if Cfg.__ENABLE_VARIABLE_TYPECHECK__:
            if varType in Cfg.list_of_dataTypes:
                elem['dataType'] = varType
            else:
                self.logWindow(TS.LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_INVALID_DATATYPE.format(varLine, varType))
                continue #with next line
        else:
            elem['dataType'] = varType
        
        listOfVariables.append(elem)
        
    if len(listOfVariables) == 0:
        return None
    else:
        return listOfVariables
    
    
    