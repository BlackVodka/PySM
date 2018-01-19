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

"""Functions for generating the state machine's source file.

This module provides functions for generating the state machine's
source file.
Basically, it creates in it's main function the source file itself
and calls subfunctions for generating each needed part of the file.
Only extern needed function should be GenerateSourceFile().
Subfunctions in this module won't be described, as they just write
file sections and should be self-explaining.
"""

from script import Template_strings as TS
from script import GenSourceTemplates as GEN
import PySM_Cfg as Cfg
import os, traceback, time


def GenerateSourceFile(self, states, transitions, config):
    """Generate source file

    This is the main function, generating the state machine's source file.

    Args:
        states: A list of processed state elements. 
        A processed state element is a dict containing
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_entry_instructions" : None or list of entry instruction text lines,
            "list_of_during_instructions" : None or list of during instruction text lines,
            "list_of_exit_instructions" : None or list of exit instruction text lines,
            "is_init_state" : True or False, marking the initial state
        transitions: A list of processed transition elements.
        A processed transition element is a dict containing
            'edge_id' : Transition Id,
            'sourceNode' : Transition start node,
            'targetNode' : Transition target node,
            'transitionCondition' : None or a list of transition condition lines
            'transitionAction' : None or a list of transition action lines
            'transitionPriority' : The transition priority as string (1,2,3...)
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
    
    cFile = OpenSourceFile(self)
    if cFile is None:
        return None
    
    # Write file header
    WriteSourceFileHeader(self, cFile)
    # Write state function prototypes
    WriteStateFunctionPrototypes(self, cFile, states)
    # Write state machine variable reset function prototype
    if config['variables'] is not None:
        WriteStateMachineVariableResetPrototype(self, cFile)
    # Create warnings if two or more transitions leaving a state
    # having the same priorities
    CheckTransitionPriorities(self, states, transitions)
    # Get needed data of TAF and TTF objects
    listOfTtfObjects = CreateTtfTafObjects(self, states, transitions, 'ttf')
    listOfTafObjects = CreateTtfTafObjects(self, states, transitions, 'taf')
    # Write transition test function prototypes, if needed
    if listOfTtfObjects is not None:
        WriteTransitionTestPrototypes(self, cFile, listOfTtfObjects)
    # Write transition actions function prototypes, if needed
    if listOfTafObjects is not None:
        WriteTransitionActionPrototypes(self, cFile, listOfTafObjects)
    # Write state objects
    WriteStateObjects(self, cFile, states)
    # Write state object pointer array
    WriteStateObjectPointerArray(self, cFile, states)
    # Write state transitions array
    WriteStateTransitionArray(self, cFile, states, transitions, listOfTtfObjects, listOfTafObjects)
    # Write state machine object
    WriteStateMachineObject(self, cFile, states, transitions, config)
    # Write static variables
    WriteLocalVariables(self, cFile, config)
    # Write implementation of state machine variable reset function
    if config['variables'] is not None:
        WriteResetVariableFunction(self, cFile, config)
    # Write implementation of state functions
    WriteStateFunctions(self, cFile, states)
    # Write implementation of transition test (TTF) functions, if needed
    if listOfTtfObjects is not None:
        WriteTtfFunctions(self, cFile, listOfTtfObjects)
    # Write implementation of transition action (TAF) functions, if needed
    if listOfTafObjects is not None:
        WriteTafFunctions(self, cFile, listOfTafObjects)
    # Write implementation of API functions
    WriteApiFunctions(self, cFile, config)
    
    
    cFile.close()
    #return tuple of header file name and full path, otherwise None will be returned
    fileName = self.txtStateMachineName.text()
    fileName = fileName[0].upper() + fileName[1:] + '.c'
    genResult = (fileName, os.path.realpath(cFile.name))
    return genResult



def OpenSourceFile(self):
    
    # try opening source file for writing, first character will be uppercase
    cFileName = self.txtStateMachineName.text() + '.c'
    cFileName = cFileName[0].upper() + cFileName[1:]
    filePath = os.path.join(self.txtGenOutputPath.text(), cFileName)
    try:
        cFile = open(filePath, 'w')
    except:
        self.logWindow(TS.LOG_WINDOW_GENERATOR_ERROR_OPENING_OUTPUT_FILE.format( self.txtGenOutputPath.text() + cFileName) )
        traceback.print_exc()
        return None
    
    return cFile

def WriteSourceFileHeader(self, cFile):
    SM_name = self.txtStateMachineName.text()
    
    try:
        headerTemplate = open(self.txtPathToHeaderTemplate.text(), 'r')
    except:
        headerTemplate = None
        self.logWindow(TS.LOG_WINDOW_GENERATOR_PROBLEM_OPENING_HEADER_TEMPLATE_FILE.format(self.txtPathToHeaderTemplate.text()))
    
    if headerTemplate is not None:
        for line in headerTemplate:
            cFile.write(line)
        headerTemplate.close()
    
    cFile.write(GEN.GENERATED_FILE_DOXYGEN_HEADER.format(
        SM_name[0].upper() + SM_name[1:] + '.c',
        self.txtAuthorName.text(),
        time.strftime("%Y-%m-%d"),
        SM_name,
        time.strftime("%Y-%m-%d"),
        time.strftime("%H:%M:%S")
        ) + '\n')
    
    SM_name = SM_name[0].upper() + SM_name[1:] 
    cFile.write(GEN.GENERATED_FILE_SOURCE_INCLUDE_HEADING + '\n')
    cFile.write('#include "' + SM_name + '.h"\n')
    cFile.write('\n')
        
    return

def WriteStateFunctionPrototypes(self, cFile, states):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_FUNCTION_PROTOTYPE_HEADING + '\n')
    for state in states:
        # always generate entry prototypes
        cFile.write( ('static void {}_SF_{}_entry(void);\n').format(SM_name, state['state_name']) )
        if state['list_of_during_instructions'] is not None:
            cFile.write( ('static void {}_SF_{}(void);\n').format(SM_name, state['state_name']) )
        if state['list_of_exit_instructions'] is not None:
            cFile.write( ('static void {}_SF_{}_exit(void);\n').format(SM_name, state['state_name']) )
            
    cFile.write('\n')
    
    return

def WriteStateMachineVariableResetPrototype(self, cFile):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_MACHINE_VARIABLE_RESET_HEADING + '\n')
    cFile.write( ('static void {}_variableResetFunction(void);\n').format(SM_name) )
            
    cFile.write('\n')
    
    return

def WriteTransitionTestPrototypes(self, cFile, ttf_list):
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_TRANSITION_TEST_FUNCTION_PROTOTYPE_HEADING + '\n')
    
    for ttf in ttf_list:
        cFile.write('static ' + Cfg.transitionTestFunctionReturnType + ' ' + ttf['name'] + '(void)' + ';\n')
    cFile.write('\n')
        
    return

def WriteTransitionActionPrototypes(self, cFile, taf_list):
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_TRANSITION_ACTION_FUNCTION_PROTOTYPE_HEADING + '\n')
    
    for taf in taf_list:
        cFile.write('static ' + Cfg.transitionActionFunctionReturnType + ' ' + taf['name'] + '(void)' + ';\n')
    cFile.write('\n')
        
    return

def WriteStateObjects(self, cFile, states):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_OBJECT_HEADING + '\n')
    for state in states:
        cFile.write('static const ' + Cfg.lib_stateType + ' ' + SM_name + '_state_' + state['state_name'] + ' =\n')
        cFile.write('{\n')
        if Cfg.__ENABLE_C99_SUPPORT__:
            cFile.write('\t\t' + '.onEntryState = ')
        else:
            cFile.write('\t\t')
        # write always entry instructions
        cFile.write(SM_name + '_SF_' + state['state_name'] + '_entry' + ',\n')

        if Cfg.__ENABLE_C99_SUPPORT__:
            cFile.write('\t\t' + '.onState = ')
        else:
            cFile.write('\t\t')
        if state['list_of_during_instructions'] is not None:
            cFile.write(SM_name + '_SF_' + state['state_name'] + ',\n')
        else:
            cFile.write(Cfg.lib_nullPtr + ',\n')
        
        if Cfg.__ENABLE_C99_SUPPORT__:
            cFile.write('\t\t' + '.onExitState = ')
        else:
            cFile.write('\t\t')
        if state['list_of_exit_instructions'] is not None:
            cFile.write(SM_name + '_SF_' + state['state_name'] + '_exit' + '\n')
        else:
            cFile.write(Cfg.lib_nullPtr + '\n')
        cFile.write('};\n\n')
    
    return

def WriteStateObjectPointerArray(self, cFile, states):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_POINTER_ARRAY_HEADING + '\n')
    cFile.write('static const ' + Cfg.lib_stateType + '* ' + SM_name + '_states_pa' + ('[{}]').format(len(states)) + ' =\n')
    cFile.write('{\n')
    for n,state in enumerate(states):
        cFile.write('\t\t' + '&' + SM_name + '_state_' + state['state_name'])
        if n < (len(states))-1:
            cFile.write(',\n')
        else:
            cFile.write('\n')
    cFile.write('};\n\n')
    
    return

def WriteStateTransitionArray(self, cFile, states, transitions, ttfs, tafs):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_TRANSITIONS_ARRAY_HEADING + '\n')
    cFile.write('static ' + Cfg.lib_transitionType + ' ' + SM_name + '_transitions_sa' + ('[{}]').format(len(transitions)) + ' = \n')
    cFile.write('{\n')
    
    for n,trans in enumerate(transitions):
        cFile.write('\t{\n')
        # source state
        cFile.write('\t\t' + '&' + SM_name + '_state_' + GetStateNameById(self, states, trans['sourceNode']) + ',\n')
        # target state
        cFile.write('\t\t' + '&' + SM_name + '_state_' + GetStateNameById(self, states, trans['targetNode']) + ',\n')
        # write TTF, if needed
        foundTtf = False
        if ttfs is not None:
            for ttf in ttfs:
                if ttf['edge_id'] == trans['edge_id']:
                    foundTtf = True
                    cFile.write('\t\t' + ttf['name'] + ',\n')
                    break
        if not foundTtf:
            cFile.write('\t\t' + Cfg.lib_nullPtr + ',\n')
        # write transition priority
        cFile.write('\t\t' + ('({})').format(Cfg.lib_transitionPrioType) + trans['transitionPriority'] + 'u,\n' )
        # write TAF, if needed
        foundTaf = False
        if tafs is not None:
            for taf in tafs:
                if taf['edge_id'] == trans['edge_id']:
                    foundTaf = True
                    cFile.write('\t\t' + taf['name'] + '\n')
                    break
        if not foundTaf:
            cFile.write('\t\t' + Cfg.lib_nullPtr + '\n')
        
        if n < (len(transitions)-1):
            cFile.write('\t},\n')
        else:
            cFile.write('\t}\n')
    cFile.write('};\n\n')
    
    return

def WriteStateMachineObject(self, cFile, states, transitions, config):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_MACHINE_OBJECT_HEADING + '\n')
    cFile.write(Cfg.lib_stateMachineType + ' ' + SM_name + '_stateMachine_s' + ' = ' + '\n')
    cFile.write('{\n')
    # Find init state
    initState = None
    for state in states:
        if state['is_init_state']:
            initState = state['state_name']
            break
    # initial state
    cFile.write('\t&' + SM_name + '_state_' + initState + ',\n')
    # current state
    cFile.write('\t&' + SM_name + '_state_' + initState + ',\n')
    # states pointer
    cFile.write('\t' + SM_name + '_states_pa' + ',\n')
    # nOfStates
    cFile.write('\t' + str(len(states)) + 'u' + ',\n')
    # Transitions array
    cFile.write('\t' + SM_name + '_transitions_sa' + ',\n')
    # nOfTransitions
    cFile.write('\t' + str(len(transitions)) + 'u' + ',\n')
    # Run entry action of initial state, always neccessary#
    # for setting the actual state static variable
    cFile.write('\t' + Cfg.lib_true + ',\n')

    # Reset SM function, if needed
    if config['variables'] is not None:
        cFile.write('\t' + SM_name + '_variableResetFunction' + '\n')
    else:
        cFile.write('\t' + Cfg.lib_nullPtr + '\n')
    cFile.write('};\n\n')
    
    return

def WriteLocalVariables(self, cFile, config):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATIC_VARIABLES_HEADING + '\n')
    # In- and output signals
    if config['inputSignals'] is not None:
        cFile.write('static ' + SM_name + '_inputSignalsType* ' + SM_name + '_inputSignals' + ';\n')
    if config['outputSignals'] is not None:
        cFile.write('static ' + SM_name + '_outputSignalsType* ' + SM_name + '_outputSignals' + ';\n')
    # Active state variable
    cFile.write('static ' + SM_name + '_' + Cfg.lib_activeStateType + ' ' + SM_name + '_activeState' + ' = ' + SM_name.upper() + '_UNINITALIZED_STATE_MACHINE' + ';\n')
    cFile.write('\n')
    # User variables
    if config['variables'] is not None:
        for line in config['variables']:
            if line['preceedingKeyWord'] is not None:
                cFile.write('static ' + line['preceedingKeyWord'] + ' ' + line['dataType'] + ' ' + line['variableName'] + ' = ' + line['initialValue'] + ';\n')
            else:
                cFile.write('static ' + line['dataType'] + ' ' + line['variableName'] + ' = ' + line['initialValue'] + ';\n')
    cFile.write('\n')
    
    return

def WriteResetVariableFunction(self, cFile, config):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_MACHINE_VARIABLE_RESET_IMPLEMENTATION_HEADING + '\n')
    cFile.write('static void ' + SM_name + '_variableResetFunction(void)\n')
    cFile.write('{\n')
    for l in config['variables']:
        cFile.write('\t' + l['variableName'] + ' = ' + l['initialValue'] + ';\n')
    cFile.write('}\n')
    cFile.write('\n')
    
    return
    
def WriteStateFunctions(self, cFile, states):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_STATE_FUNCTION_IMPLEMENTATION_HEADING + '\n')
    for state in states:
        # entry will be generated everytime for setting the current state static variable
        cFile.write('static void ' + SM_name + '_SF_' + state['state_name'] + '_entry' + '(void)' + '\n')
        cFile.write('{\n')
        cFile.write('\t' + SM_name + '_activeState' + ' = ' + SM_name.upper() + '_' + state['state_name'] + ';\n')
        if state['list_of_entry_instructions'] is not None:
            for line in state['list_of_entry_instructions']:
                cFile.write('\t' + line + '\n')
        cFile.write('}\n\n')
        # during, if needed
        if state['list_of_during_instructions'] is not None:
            cFile.write('static void ' + SM_name + '_SF_' + state['state_name'] + '(void)' + '\n')
            cFile.write('{\n')
            for line in state['list_of_during_instructions']:
                cFile.write('\t' + line + '\n')
            cFile.write('}\n\n')
        # exit, if needed
        if state['list_of_exit_instructions'] is not None:
            cFile.write('static void ' + SM_name + '_SF_' + state['state_name'] + '_exit' + '(void)' + '\n')
            cFile.write('{\n')
            for line in state['list_of_exit_instructions']:
                cFile.write('\t' + line + '\n')
            cFile.write('}\n\n')
    
    cFile.write('\n')
    return

def WriteTtfFunctions(self, cFile, ttfs):

    cFile.write(GEN.GENERATED_FILE_SOURCE_TTF_IMPLEMENTATION_HEADING + '\n')
    
    for ttf in ttfs:
        cFile.write('static ' + Cfg.transitionTestFunctionReturnType + ' ' + ttf['name'] + '(void)' + '\n')
        cFile.write('{\n')
        cFile.write('\t' + Cfg.transitionTestFunctionReturnType + ' ' + 'rtrn = (' + '\n')
        for ttfLine in ttf['text']:
            cFile.write('\t\t' + ttfLine + '\n')
        cFile.write('\t\t' + ');' + '\n')
        cFile.write('\t' + 'return rtrn' + ';\n')
        cFile.write('}\n\n')
    
    return

def WriteTafFunctions(self, cFile, tafs):

    cFile.write(GEN.GENERATED_FILE_SOURCE_TAF_IMPLEMENTATION_HEADING + '\n')
    
    for taf in tafs:
        cFile.write('static ' + Cfg.transitionActionFunctionReturnType + ' ' + taf['name'] + '(void)' + '\n')
        cFile.write('{\n')
        for tafLine in taf['text']:
            cFile.write('\t' + tafLine + '\n')
        cFile.write('}\n\n')
    
    cFile.write('\n')
    return

def WriteApiFunctions(self, cFile, config):
    SM_name = self.txtStateMachineName.text()
    
    cFile.write(GEN.GENERATED_FILE_SOURCE_API_IMPLEMENTATION_HEADING + '\n')
    # State machine main function
    ###############################
    cFile.write(Cfg.lib_returnType + ' ' + SM_name[0].upper() + SM_name[1:] + '_mainFunction(')
    if (config['inputSignals'] is None) and ((config['outputSignals'] is None)):
        cFile.write('void')
    else:
        if config['inputSignals'] is not None:
            cFile.write(SM_name + '_inputSignalsType* swc_inputSignals')
        if config['outputSignals'] is not None:
            if config['inputSignals'] is not None:
                cFile.write(',\n' + '\t\t')
            cFile.write(SM_name + '_outputSignalsType* swc_outputSignals')
    cFile.write(')\n')
    
    cFile.write('{\n')
    cFile.write('\t' + Cfg.lib_returnType + ' ' + 'runStateMachineResult' + ';\n')
    cFile.write('\n')
    if config['inputSignals'] is not None:
        cFile.write('\t' + SM_name + '_inputSignals = swc_inputSignals' + ';\n')
    if config['outputSignals'] is not None:
        cFile.write('\t' + SM_name + '_outputSignals = swc_outputSignals' + ';\n')
    cFile.write('\n')
    cFile.write('\t' + 'runStateMachineResult = ' + Cfg.lib_runStateMachine + '(&' + SM_name + '_stateMachine_s' + ');\n')
    cFile.write('\t' + 'return runStateMachineResult' + ';\n')
    cFile.write('}\n\n')
    
    # Getter function of active state
    ###################################
    cFile.write('void ' + SM_name[0].upper() + SM_name[1:] + '_getActiveState(' + SM_name + '_' + Cfg.lib_activeStateType + '* swc_activeState' + ')\n')
    cFile.write('{\n')
    cFile.write('\t' + '*swc_activeState = ' + SM_name + '_activeState' + ';\n')
    cFile.write('}\n\n')
    
    return


def CreateTtfTafObjects(self, states, transitions, transType):
    SM_name = self.txtStateMachineName.text()
    listOfObjects = []
    
    
    if transType == 'ttf':
        kw = 'transitionCondition'
    elif transType == 'taf':
        kw = 'transitionAction'
    
    for trans in transitions:
        if trans[kw] is not None:
            # find source State
            sourceState = GetStateNameById(self, states, trans['sourceNode'])
            if sourceState is None:
                self.logWindow(TS.LOG_WINDOW_GENERATOR_SOURCE_STATE_OF_TRANSITION_NOT_FOUND.format(trans['edge_id']))
                continue
            destinationState = GetStateNameById(self, states, trans['targetNode'])
            if destinationState is None:
                self.logWindow(TS.LOG_WINDOW_GENERATOR_DESTINATION_STATE_OF_TRANSITION_NOT_FOUND.format(trans['edge_id']))
                continue
            # Found a TTF/TAF to generate
            if transType == 'ttf':
                txt = trans['transitionCondition']
                aliasTxt = '_TTF_'
            elif transType == 'taf':
                txt = trans['transitionAction']
                aliasTxt = '_TAF_'
            ttfTafObject = {
                'name' : SM_name + aliasTxt + sourceState.upper() + '_to_' + destinationState.upper(),
                'edge_id' : trans['edge_id'],
                'text' : txt
                }
            listOfObjects.append(ttfTafObject)
    
    if not(len(listOfObjects) == 0):
        RenameDuplicatesTtfTaf(self, listOfObjects)
    else:
        return None
    
    return listOfObjects

def GetStateNameById(self, states, elemId):
    
    for state in states:
        if state['node_id'] == elemId:
            return state['state_name']
    
    return None

def RenameDuplicatesTtfTaf(self, listOfObjects):
    listOfNames = []
    foundDuplicates = False
    
    for obj in listOfObjects:
        listOfNames.append(obj['name'])
    
    names = set(listOfNames)
    
    for elem in names:
        # find all occurences of elem in listOfNames:
        indices = [i for i, x in enumerate(listOfNames) if x == elem]
        if len(indices) > 1:
            # found duplicates, rename them
            foundDuplicates = True
            for n, idx in enumerate(indices):
                listOfNames[idx] = listOfNames[idx] + '_' + str(n+1)
                
    # write back duplicates, if needed
    if foundDuplicates:
        for idx, obj in enumerate(listOfObjects):
            obj['name'] = listOfNames[idx]
    
    return

def CheckTransitionPriorities(self, states, transitions):
    
    for state in states:
        for prio in range(1, Cfg.max_number_of_transitions_per_state+1):
            nOfTransWithPrio = 0
            for trans in transitions:
                if (trans['sourceNode'] == state['node_id']) and (trans['transitionPriority'] == str(prio)):
                    nOfTransWithPrio += 1
            if nOfTransWithPrio >= 2:
                self.logWindow(TS.LOG_WINDOW_GENERATOR_TRANSITIONS_HAVE_SAME_PRIORITY.format(
                    state['node_id'], state['state_name'], str(prio)))
    
    return None
    
