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
GENERATED_FILE_HEADER_INCLUDE_GUARD = \
"""#ifndef {}_H_
#define {}_H_"""

GENERATED_FILE_HEADER_INCLUDE_HEADING = \
"""
/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */"""
GENERATED_FILE_HEADER_TYPEDEFS_HEADING = \
"""
/* ========================================================================= */
/* TYPEDEFS                                                                  */
/* ========================================================================= */"""
GENERATED_FILE_HEADER_USER_PREPROCESSOR_DIRECTIVES_HEADING = \
"""
/* ========================================================================= */
/* USER PREPROCESSOR DIRECTIVES                                              */
/* ========================================================================= */"""
GENERATED_FILE_HEADER_API_DECLARATION_HEADING = \
"""
/* ========================================================================= */
/* API DECLARATION                                                           */
/* ========================================================================= */"""
GENERATED_FILE_HEADER_DOXYGEN_INPUT_SIGNALS = \
"""
/**
 * @brief Structure defining input signals for state machine
 * {}
*/"""
GENERATED_FILE_HEADER_DOXYGEN_OUTPUT_SIGNALS = \
"""
/**
 * @brief Structure defining output signals for state machine
 * {}
*/"""
GENERATED_FILE_HEADER_DOXYGEN_STATES = \
"""
/**
 * @brief Enum for exporting current active state of state machine
 * {}
*/"""
GENERATED_FILE_TYPEDEF_STRUCT_OPENING = \
"""
typedef struct
{
"""
GENERATED_FILE_TYPEDEF_ENUM_OPENING = \
"""
typedef enum
{
"""
GENERATED_FILE_HEADER_DOXYGEN_MAIN_FUNCTION = \
"""
/**
 * @brief Main function of the state machine
 * {}
*/"""
GENERATED_FILE_HEADER_DOXYGEN_GET_CURRENT_STATE = \
"""
/**
 * @brief Main function of the state machine
 * {}
*/"""
GENERATED_FILE_HEADER_ENDING = \
"""
#endif /* {}_H_ */
"""
