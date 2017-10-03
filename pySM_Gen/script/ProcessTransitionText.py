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

"""Functions for processing transition texts

This module provides functions for processing transition texts,
e.g. finding priority, action and condition statements.
Only extern needed function should be ProcessTransitionText()
"""

from script import Template_strings as TS
import PySM_Cfg as Cfg


def ProcessTransitionText(self, transitions):
    """Process transition texts

    For easier use of the transition objects, the raw parsed
    transitions are processed and split into their containing
    informations, described in the return section below.

    Args:
        transitions: A list containing parsed transitions dicts.
        A parsed transition dictionary contains
            'edge_id' : EdgeId of the transition
            'sourceNode' : NodeId of the starting node
            'targetNode' : NodeId of the target node
            'transitionTextLines' : None or a list of transition text lines

    Returns:
        A tuple (processedTransitions, stats), with:
        processedTransitions is a list of processed transition dicts, where
        a processed transition dict contains
            'edge_id' : Transition Id,
            'sourceNode' : Transition start node,
            'targetNode' : Transition target node,
            'transitionCondition' : None or a list of transition condition lines
            'transitionAction' : None or a list of transition action lines
            'transitionPriority' : The transition priority as string (1,2,3...)
        stats is a dict containing
            "nOfConditions" : Number of transitions with condition statements,
            "nOfActions" : Number of transitions with action statements,
            "nOfBlanks" : Number of transitions without any statements at all
    """
    processedTransitions = []
    
    for currTrans in transitions:
        processedTransitionElem = {
            'edge_id' : currTrans['edge_id'],
            'sourceNode' : currTrans['sourceNode'],
            'targetNode' : currTrans['targetNode'],
            'transitionCondition' : None,
            'transitionAction' : None,
            'transitionPriority' : None
            }
        
        # First line if existent should be either an action or condition statement
        if currTrans["transitionTextLines"] is not None:
            processedTransitionElem["transitionPriority"] = GetPriority(self, currTrans)
            processedTransitionElem["transitionCondition"] = GetConditionOrAction(self, currTrans, 'condition')
            processedTransitionElem["transitionAction"] = GetConditionOrAction(self, currTrans, 'action')
        else:
            # Handle transitions without any text with highest priority
            self.logWindow(TS.LOG_WINDOW_TRANSITION_HAS_NO_PRIORITY.format(currTrans['edge_id']))
            processedTransitionElem["transitionPriority"] = '1'
        
        processedTransitions.append(processedTransitionElem)
        
    stats = GetStats(self, processedTransitions)

    return (processedTransitions, stats)

def GetPriority(self, trans):
    """Get transition priority

    Evaluates a parsed transition's text and searchs for
    the priority of a the parsed transition.

    Args:
        trans: A parsed transition dict.
        A parsed transition dictionary contains
            'edge_id' : EdgeId of the transition
            'sourceNode' : NodeId of the starting node
            'targetNode' : NodeId of the target node
            'transitionTextLines' : None or a list of transition text lines

    Returns:
        prio: Transition's priority as string (1,2,3...)
    """
    firstLine = (trans["transitionTextLines"])[0]
    prio = None
    
    for n in range(1, Cfg.max_number_of_transitions_per_state):
        if ('<' + str(n) + '>') in firstLine:
            prio = str(n)
            break
    if prio is None:
        self.logWindow(TS.LOG_WINDOW_TRANSITION_HAS_NO_PRIORITY.format(trans['edge_id']))
        prio = '1'
    elif not(int(prio) > 0):
        self.logWindow(TS.LOG_WINDOW_TRANSITION_HAS_WRONG_PRIORITY.format(trans['edge_id']))
        
    return prio

def GetConditionOrAction(self, trans, which):
    """Get transition condition or action statements

    Evaluates a parsed transition's text and searchs for
    either action or condition statements

    Args:
        trans: A parsed transition dict.
        A parsed transition dictionary contains
            'edge_id' : EdgeId of the transition
            'sourceNode' : NodeId of the starting node
            'targetNode' : NodeId of the target node
            'transitionTextLines' : None or a list of transition text lines
        which: A string, either 'condition' or 'action', telling this
        generic function if it should search for condition or action statements

    Returns:
        tempTxt: Either None, if the searched statements weren't found or
        a list of found statement lines
    """
    startTagFound = False
    endTagFound = False
    tempTxt = None
    
    if which == 'condition':
        startChar = '['
        endChar = ']'
    elif which == 'action':
        startChar = '{'
        endChar = '}'

    
    for currLine in trans["transitionTextLines"]:
        # check for condition instructions
        condStartChar = currLine.find(startChar)
        condEndChar = currLine.rfind(endChar)
        startTagFound = (condStartChar != -1)
        endTagFound = (condEndChar != -1)
        # Condition is a one liner:
        if startTagFound and endTagFound:
            if condStartChar < condEndChar:
                tempTxt = [currLine[condStartChar +1 : condEndChar]]
                break
            else:
                if which == 'condition':
                    self.logWindow(TS.LOG_WINDOW_TRANSITION_TEXT_PROCESSING_CONDITION_PROBLEM, format(trans['edge_id']))
                elif which == 'action':
                    self.logWindow(TS.LOG_WINDOW_TRANSITION_TEXT_PROCESSING_ACTION_PROBLEM, format(trans['edge_id']))
                break
        elif startTagFound:
            tempTxt = [currLine[condStartChar+1 :]]
        elif endTagFound:
            tempTxt.append(currLine[0:condEndChar])
            break
        # area between lines
        elif tempTxt is not None:
            tempTxt.append(currLine)
            
    # End tag not found but start tag:
    if (tempTxt is not None) and (not endTagFound):
        if which == 'condition':
            self.logWindow(TS.LOG_WINDOW_TRANSITION_TEXT_PROCESSING_CONDITION_PROBLEM, format(trans['edge_id']))
        elif which == 'action':
            self.logWindow(TS.LOG_WINDOW_TRANSITION_TEXT_PROCESSING_ACTION_PROBLEM, format(trans['edge_id']))
        tempTxt = None
    
    return tempTxt


def GetStats(self, processedTransitions):
    """Gets some transition processing statistics

    Gets some statistics for the processed transitions for
    logwindow output.

    Args:
        processedTransitions: A list of processed transition dicts.
        a processed transition dict contains
            'edge_id' : Transition Id,
            'sourceNode' : Transition start node,
            'targetNode' : Transition target node,
            'transitionCondition' : None or a list of transition condition lines
            'transitionAction' : None or a list of transition action lines
            'transitionPriority' : The transition priority as string (1,2,3...)

    Returns:
        A dict containing
        "nOfConditions" : Number of transitions with condition statements,
        "nOfActions" : Number of transitions with action statements,
        "nOfBlanks" : Number of transitions without any statements at all
    """
    nOfConditions = 0
    nOfActions = 0
    nOfBlanks = 0
    
    for trans in processedTransitions:
        if not(trans["transitionAction"] is None):
            nOfActions += 1
        elif not(trans["transitionCondition"] is None):
            nOfConditions += 1
        else:
            nOfBlanks += 1
            
    return {
        "nOfConditions" : nOfConditions,
        "nOfActions" : nOfActions,
        "nOfBlanks" : nOfBlanks
        }
