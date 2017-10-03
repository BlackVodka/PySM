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
#   Box is distributed in the hope that it will be useful,                   #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Lesser General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Lesser General Public         #
#   License along with Box.  If not, see <http://www.gnu.org/licenses/>.     #
##############################################################################

"""Functions for processing state texts

This module provides functions for processing state texts,
e.g. finding entry, during and exit statements.
Only extern needed function should be ProcessStateText()
"""

from script import Template_strings as TS

entry_codeWord = 'entry:'
during_codeWord = 'during:'
exit_codeWord = 'exit:'


def ProcessStateText(self, states):
    """Process state texts

    For easier use of the state objects, the raw parsed
    states are processed and split into their containing
    informations, described in the return section below.
    For being able to mix order entry, during and exit statements,
    if existent, processing is done using line numbers of
    entry, during and exit keywords.

    Args:
        states: A list containing parsed state dicts.
        A parsed state dictionary contains
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_text_lines" : None or State's contained text,
            "is_init_state" : True/False

    Returns:
        None, if a error happened or
        A tuple (ListOfProcessedStates, stats), with:
        processedStates is a list of processed state dicts, where
        a processed state dict contains
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_entry_instructions" : None or list of entry instruction text lines,
            "list_of_during_instructions" : None or list of during instruction text lines,
            "list_of_exit_instructions" : None or list of exit instruction text lines,
            "is_init_state" : True or False, marking the initial state
        stats is a dict containing
            "nOfEntries" : Number of states with entry statements,
            "nOfDurings" : Number of states with during statements,
            "nOfExits" : Number of states with exit statements
    """
    
    ListOfProcessedStates = []

    
    
    for currState in states:
        processedStateElem = {
            "node_id" : currState['node_id'],
            "state_name" : currState['state_name'],
            "list_of_entry_instructions" : None,
            "list_of_during_instructions" : None,
            "list_of_exit_instructions" : None,
            "is_init_state" : currState['is_init_state']
            }
        nOfEntryStatements = 0
        nOfDuringStatements = 0
        nOfExitStatements = 0
        entryCodewordLineNo = None
        duringCodewordLineNo = None
        exitCodewordLineNo = None
        codeWordLineNumbers = []
        
        if currState['list_of_text_lines'] is None:
            # skip this state, as it doesn't conatain any text besides the state name
            continue
        
        # Get line no. of codewords
        for currLineIdx in range(0,len(currState['list_of_text_lines'])):
            currLine = (currState['list_of_text_lines'])[currLineIdx]
            if entry_codeWord in currLine:
                entryCodewordLineNo = currLineIdx
                nOfEntryStatements += 1
                continue
            elif during_codeWord in currLine:
                duringCodewordLineNo = currLineIdx
                nOfDuringStatements += 1
                continue           
            elif exit_codeWord in currLine:
                exitCodewordLineNo = currLineIdx
                nOfExitStatements += 1
                continue
            
        if (nOfEntryStatements > 1) or (nOfDuringStatements > 1) or (nOfExitStatements > 1):
            TS.LOG_WINDOW_ERROR_STATE_TEXT_CONTAINS_DUPLICATE_CODEWORDS.format(
                currState['state_name'], currState['node_id'], nOfEntryStatements,nOfDuringStatements, nOfExitStatements)
            return None
            
        
        tempList = [entryCodewordLineNo, duringCodewordLineNo, exitCodewordLineNo]
        for elem in tempList:
            if elem is not None:
                codeWordLineNumbers.append(elem)
                
        if len(codeWordLineNumbers) == 0:
            TS.LOG_WINDOW_WARNING_STATE_TEXT_CONTAINS_NO_CODEWORDS.format(
                currState['state_name'], currState['node_id'])
            continue
        
        #When reaching this point, the state contains at least one codeword, let's process it:
        if entryCodewordLineNo is not None:
            processedStateElem['list_of_entry_instructions'] = \
                GetInstructionText(self, entryCodewordLineNo, codeWordLineNumbers, currState)
        
        if duringCodewordLineNo is not None:
            processedStateElem['list_of_during_instructions'] = \
                GetInstructionText(self, duringCodewordLineNo, codeWordLineNumbers, currState)
                
        if exitCodewordLineNo is not None:
            processedStateElem['list_of_exit_instructions'] = \
                GetInstructionText(self, exitCodewordLineNo, codeWordLineNumbers, currState)
        
        # getInstructionText returns False if something has gone wrong ( [Error] )
            if (processedStateElem['list_of_entry_instructions'] == False) or \
                (processedStateElem['list_of_during_instructions'] == False) or \
                (processedStateElem['list_of_exit_instructions'] == False):
                return None
            
        ListOfProcessedStates.append(processedStateElem)
    
    stats = GetProcessedStatesStats(self, ListOfProcessedStates)
    return (ListOfProcessedStates, stats)


def GetInstructionText(self, currCodeWordLineNo, codeWordLineNums, currState):
    """Gets instruction text between codewords (entry, during, exit)

    Gets text between state codewords
    Args:
        currCodeWordLineNo: Line number (in the states' text) of
        the currently handled state codeword as int
        codeWordLineNums: A list of the state codeword's line numbers
        currState: Current processed parsed state dict, containing
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_text_lines" : None or State's contained text,
            "is_init_state" : True/False

    Returns:
        False, if an error happened or
        txtLst : A list of the found state instruction lines
    """
    
    currIdx = currCodeWordLineNo

            
    # Catch error of directly following codewords
    if (currIdx +1) in codeWordLineNums:
        self.logWindow(TS.LOG_WINDOW_ERROR_STATE_TEXT_DIRECTLY_FOLLOWING_CODEWORDS.format(currState['state_name'], currState['node_id']))
        return False
    
    # Catch error of no text after codeword
    if (currIdx+1) == len(currState['list_of_text_lines']):
        self.logWindow(TS.LOG_WINDOW_ERROR_STATE_NO_TEXT_AFTER_CODEWORD.format(currState['state_name'], currState['node_id']))
        return False

    currIdx += 1 # point to first instruction line
    txtLst = []
    while not((currIdx in codeWordLineNums) or (currIdx == len(currState['list_of_text_lines']) )) :
        txtLst.append( (currState['list_of_text_lines'])[currIdx] )
        currIdx += 1

    return txtLst


def GetProcessedStatesStats(self, states):
    """Gets some state processing statistics

    Gets some statistics for the processed states for
    logwindow output.

    Args:
       states: A list of processed state dicts.
        a processed state dict contains
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_entry_instructions" : None or a list of instruction statement lines,
            "list_of_during_instructions" : None or a list of during statement lines,
            "list_of_exit_instructions" : None or a list of exit statement lines,
            "is_init_state" : True or False, marking the initial state

    Returns:
        A dict containing
        "nOfEntries" : Number of states with entry statements,
        "nOfDurings" : Number of states with during statements,
        "nOfExits" : Number of states with exit statements
    """
    nOfEntries = 0
    nOfDurings = 0
    nOfExits = 0
    
    for currS in states:
        if currS["list_of_entry_instructions"] is not None:
            nOfEntries += 1
            continue
        if currS["list_of_during_instructions"] is not None:
            nOfDurings += 1
            continue
        if currS["list_of_exit_instructions"] is not None:
            nOfExits += 1
            continue
    
    return {
        "nOfEntries" : nOfEntries,
        "nOfDurings" : nOfDurings,
        "nOfExits" : nOfDurings
        }
        