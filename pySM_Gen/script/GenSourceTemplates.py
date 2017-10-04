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

GENERATED_FILE_DOXYGEN_HEADER = \
"""
/**
 * @file {}
 * @author {}
 * @date {}
 * @brief Header for generated state machine {}
 * Generated {} {} by PySM - The python state machine generator.
 */
 """
 
GENERATED_FILE_SOURCE_INCLUDE_HEADING = \
"""
/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_FUNCTION_PROTOTYPE_HEADING = \
"""
/* ========================================================================= */
/* STATE FUNCTION (SF) PROTOTYPES                                            */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_MACHINE_VARIABLE_RESET_HEADING = \
"""
/* ========================================================================= */
/* STATE MACHINE VARIABLE RESET FUNCTION                                     */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_TRANSITION_TEST_FUNCTION_PROTOTYPE_HEADING = \
"""
/* ========================================================================= */
/* STATE TRANSITION TEST FUNCTION (TTF) PROTOTYPES                           */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_TRANSITION_ACTION_FUNCTION_PROTOTYPE_HEADING = \
"""
/* ========================================================================= */
/* STATE TRANSITION ACTION FUNCTION (TAF) PROTOTYPES                         */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_OBJECT_HEADING = \
"""
/* ========================================================================= */
/* CREATION OF STATE OBJECTS                                                 */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_POINTER_ARRAY_HEADING = \
"""
/* ========================================================================= */
/* CREATION OF STATE OBJECT POINTER ARRAY                                    */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_TRANSITIONS_ARRAY_HEADING = \
"""
/* ========================================================================= */
/* CREATION OF STATE TRANSITIONS ARRAY                                       */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_MACHINE_OBJECT_HEADING = \
"""
/* ========================================================================= */
/* CREATION OF STATE MACHINE OBJECT                                          */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATIC_VARIABLES_HEADING = \
"""
/* ========================================================================= */
/* DE- AND INITALIZATION OF MODULE LOCAL (STATIC) VARIABLES                  */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_MACHINE_VARIABLE_RESET_IMPLEMENTATION_HEADING = \
"""
/* ========================================================================= */
/* IMPLEMENTATION : STATE MACHINE VARIABLE RESET FUNCTION                    */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_STATE_FUNCTION_IMPLEMENTATION_HEADING = \
"""
/* ========================================================================= */
/* IMPLEMENTATION : STATE FUNCTIONS                                          */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_TTF_IMPLEMENTATION_HEADING = \
"""
/* ========================================================================= */
/* IMPLEMENTATION : TRANSITION TEST FUNCTIONS (TTFs)                         */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_TAF_IMPLEMENTATION_HEADING = \
"""
/* ========================================================================= */
/* IMPLEMENTATION : TRANSITION ACTION FUNCTIONS (TAFs)                       */
/* ========================================================================= */"""
GENERATED_FILE_SOURCE_API_IMPLEMENTATION_HEADING = \
"""
/* ========================================================================= */
/* IMPLEMENTATION : API FUNCTIONS                                            */
/* ========================================================================= */"""


