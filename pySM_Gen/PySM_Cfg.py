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
__ENABLE_VARIABLE_TYPECHECK__ = False

default_code_header_file = 'defaultCodeHeader.txt'
default_author_name = 'Author'
default_output_path = 'OUT'
max_number_of_transitions_per_state = 10
logfile_name = 'PySM_Gen.log'
list_of_dataTypes = [
    'pySm_bool', 'pySm_uint8', 'pySm_int8', 'pySm_uint16', 'pySm_int16', 'pySm_uint32', 'pySm_int32', 'pySm_uint64', 'pySm_int64']
# {} will be replaced by given state machine name
inputSignalPrefix = "{}_inputSignals->"
outputSignalPrefix = "{}_outputSignals->"
lib_typeFileName = 'PySm_types.h'
lib_mainHeaderName = 'PySm.h'
lib_stateType = 'pySm_stateType'
lib_transitionType = 'pySm_stateTransitionType'
lib_nullPtr = 'PYSM_NULL_PTR'
lib_transitionPrioType = 'pySm_transitionPriorityType'
lib_stateMachineType = 'pySm_stateMachineType'
lib_activeStateType = 'activeStateType'
lib_returnType = 'pySm_returnType'
lib_true = 'PYSM_TRUE'
lib_false =  'PYSM_FALSE'
lib_runStateMachine = 'PySm_runStateMachine'
transitionTestFunctionReturnType = 'pySm_bool'
transitionActionFunctionReturnType = 'void'

