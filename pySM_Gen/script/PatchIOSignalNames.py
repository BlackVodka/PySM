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

import PySM_Cfg as Cfg


def Patch_states(self, states, config):
    """Patch state texts

    For using in-/output signals later in the generated code,
    these signals need a special prefix PySM_Cfg.py : in-/outputSignalPrefix.
    To avoid taking care of this later when doing the code generation,
    the state texts will be patched before and all occurences of
    in-/outputsignals will get the additional prefix.

    Args:
        states: A list containing processed state dictionarys.
        A processed state dictionary contains
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_entry_instructions" : None or a list of entry instruction lines
            "list_of_during_instructions" : None or a list of during instruction lines
            "list_of_exit_instructions" : None or a list if exit instruction lines
            "is_init_state" : True or False
        config: A dictionary of the processed configuration:
            'preprocessorInstructions' : None or a list of preprocessor instruction lines,
            'variables' : None or a list of dictionarys:
                'dataType' : A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The variable's name,
                'initialValue' : The variable's initial value (as string)
            'inputSignals' : None or a list of dictionarys:
                'dataType': A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The input signal's name
            'outputSignals' : None or a list of dictionarys:
                'dataType': A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The output signal's name

    Returns:
        A tuple (nOfPatchedStates, nOfPatchedElems) as numbers for statistic
        outputs in the logwindow.
    """

    nOfPatchedStates = 0
    nOfPatchedElems = 0
    stateEntries = ["list_of_entry_instructions", "list_of_during_instructions", "list_of_exit_instructions"]
    inPrefix = Cfg.inputSignalPrefix.format(self.txtStateMachineName.text())
    outPrefix = Cfg.outputSignalPrefix.format(self.txtStateMachineName.text())


    for stateNo in range(len(states)):
        state = states[stateNo]
        patched = False
        
        for stateEntry in stateEntries:
            if state[stateEntry] is not None:
                for entryLineNo in range(len(state[stateEntry])):
                    entryLine = (state[stateEntry])[entryLineNo]
                    # check if in or output signals are mentioned
                    if config["inputSignals"] is not None:
                        for inVar in config["inputSignals"]:
                            # found a entry for an input signal
                            if inVar["variableName"] in entryLine:
                                ((states[stateNo])[stateEntry])[entryLineNo] = entryLine.replace( inVar["variableName"], inPrefix + inVar["variableName"] )
                                patched = True
                                nOfPatchedElems += 1
                                
                    if config["outputSignals"] is not None:
                        for outVar in config["outputSignals"]:
                            # found a entry for an input signal
                            if outVar["variableName"] in entryLine:
                                ((states[stateNo])[stateEntry])[entryLineNo] = entryLine.replace( outVar["variableName"], outPrefix + outVar["variableName"] )
                                patched = True
                                nOfPatchedElems += 1
        if patched:
            nOfPatchedStates += 1
            
    return(nOfPatchedStates, nOfPatchedElems)


def Patch_transitions(self, transitions, config):
    """Patch transition texts

    For using in-/output signals later in the generated code,
    these signals need a special prefix PySM_Cfg.py : in-/outputSignalPrefix.
    To avoid taking care of this later when doing the code generation,
    the transition texts will be patched before and all occurences of
    in-/outputsignals will get the additional prefix.

    Args:
        transitions: A list containing processed transition dictionarys.
        A processed transition dictionary contains
            'edge_id' : The transition's Id,
            'sourceNode' : The transitions start node,
            'targetNode' : The transitions target node,
            'transitionCondition' : None or a list of transition condition lines,
            'transitionAction' : None or a list of transition action lines,
            'transitionPriority' : Transition priority as string (1,2,3,4...)
        config: A dictionary of the processed configuration:
            'preprocessorInstructions' : None or a list of preprocessor instruction lines,
            'variables' : None or a list of dictionarys:
                'dataType' : A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The variable's name,
                'initialValue' : The variable's initial value (as string)
            'inputSignals' : None or a list of dictionarys:
                'dataType': A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The input signal's name
            'outputSignals' : None or a list of dictionarys:
                'dataType': A entry of PySM_Cfg.py : list_of_dataTypes,
                'variableName' : The output signal's name

    Returns:
        A tuple (nOfPatchedTransitions, nOfPatchedElems) as numbers for statistic
        outputs in the logwindow.
    """

    nOfPatchedTransitions = 0
    nOfPatchedElems = 0
    transitionEntries = ["transitionCondition", "transitionAction"]
    inPrefix = Cfg.inputSignalPrefix.format(self.txtStateMachineName.text())
    outPrefix = Cfg.outputSignalPrefix.format(self.txtStateMachineName.text())


    for transNo in range(len(transitions)):
        trans = transitions[transNo]
        patched = False
        
        for transEntry in transitionEntries:
            if trans[transEntry] is not None:
                for entryLineNo in range(len(trans[transEntry])):
                    entryLine = (trans[transEntry])[entryLineNo]
                    # check if in or output signals are mentioned
                    if config["inputSignals"] is not None:
                        for inVar in config["inputSignals"]:
                            # found a entry for an input signal
                            if inVar["variableName"] in entryLine:
                                ((transitions[transNo])[transEntry])[entryLineNo] = entryLine.replace( inVar["variableName"], inPrefix + inVar["variableName"] )
                                patched = True
                                nOfPatchedElems += 1
                                
                    if config["outputSignals"] is not None:
                        for outVar in config["outputSignals"]:
                            # found a entry for an input signal
                            if outVar["variableName"] in entryLine:
                                ((transitions[transNo])[transEntry])[entryLineNo] = entryLine.replace( outVar["variableName"], outPrefix + outVar["variableName"] )
                                patched = True
                                nOfPatchedElems += 1
        if patched:
            nOfPatchedTransitions += 1
            
    return(nOfPatchedTransitions, nOfPatchedElems)


