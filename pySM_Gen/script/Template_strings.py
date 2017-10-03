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
#   Box is distributed in the hope that it will be useful,                   #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Lesser General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Lesser General Public         #
#   License along with Box.  If not, see <http://www.gnu.org/licenses/>.     #
##############################################################################


LOG_WINDOW_GENERATION_STARTED = \
    '********************************************* GENERATION STARTED *********************************************\n'
LOG_WINDOW_GENERATION_ERROR = \
    '********************************************* GENERATION ABORTED *********************************************\n'
LOG_WINDOW_GENERATION_FINISHED = \
    '******************************************** GENERATION FINISHED *********************************************\n'
LOG_WINDOW_ERROR_OPENING_LOGFILE = \
'[Warning] Error opening logfile {} for generation output\n'
LOG_WINDOW_NO_YED_INPUT_FILE_GIVEN = \
'[Error] Generation aborted, no yEd input file specified.\n'
LOG_WINDOW_NO_STATEMACHINE_NAME_GIVEN = \
'[Error] Generation aborted, no state machine name specified.\n'
LOG_WINDOW_USING_DEFAULT_HEADER_FILE = \
'[Info] No code generation header specified, will use the default one: '
LOG_WINDOW_USING_DEFAULT_AUTHOR_NAME = \
'[Info] No author name specified, will use the default one: '
LOG_WINDOW_USING_DEFAULT_OUTPUT_DIR = \
'[Info] No output directory specified, will use the default one: '
LOG_WINDOW_ERROR_OPENING_YED_INPUT_FILE = \
"[Error] Generation aborted, given yEd input file could not be opened\n"
LOG_WINDOW_PARSING_IN_PROGRESS = \
"[Info] Started parsing given input graphml file:\n{}\n"
LOG_WINDOW_ERROR_PARSING_STATE_NAME = \
"[Error] Generation aborted, problem parsing state name of node_id {} (read first line: {})\n"
LOG_WINDOW_WARNING_STATE_HAS_ONLY_NAME = \
"[Warning] state with node_id {} (first_line {}) contains only one line of text (state name?)\n"
LOG_WINDOW_ERROR_PARSING_CONFIG_BLOCK = \
"[Error] Generation aborted, problem parsing config block node_id {} (read first line: {})\n"
LOG_WINDOW_ERROR_PARSING_NO_INIT_STATE_MARKER = \
"[Error] Generation aborted, wasn\'t able to find a marker for the initial state\n"
LOG_WINDOW_ERROR_PARSING_INIT_STATE_NOT_FOUND = \
"[Error] Generation aborted, wasn\'t able to find the state connected to the init state marker\n"
LOG_WINDOW_ERROR_PARSING_NO_STATES_FOUND = \
"[Error] Generation aborted, wasn\'t able to find any state at all\n"
LOG_WINDOW_ERROR_PARSING_NO_TRANSITIONS_FOUND = \
"[Error] Generation aborted, wasn\'t able to find any transitions at all\n"
LOG_WINDOW_ERROR_PARSING_NO_STATE_TEXT_FOUND = \
"[Error] Generation aborted, in state with id {} no text could be found\n"
LOG_WINDOW_FINISHED_PARSING = \
"[Info] Finished parsing graphml file, found {} states, {} configuration blocks, {} transitions\n" 
LOG_WINDOW_STATE_TEXT_PROCESSING_IN_PROGRESS = \
"[Info] Started processing the state texts\n"
LOG_WINDOW_ERROR_STATE_TEXT_DIRECTLY_FOLLOWING_CODEWORDS = \
"[Error] Unable to process text of state {} (node_id {}), some codewords are directly following up each other\n"
LOG_WINDOW_ERROR_STATE_TEXT_CONTAINS_DUPLICATE_CODEWORDS = \
"[Error]State {} (node_id {}) contains duplicate codewords (entries: {}, durings: {}, exits: {})\n"
LOG_WINDOW_WARNING_STATE_TEXT_CONTAINS_NO_CODEWORDS = \
"[Warning] Wasn\'t able to find any codeword in State {} (node_id {}) at all\n"
LOG_WINDOW_ERROR_STATE_NO_TEXT_AFTER_CODEWORD = \
"[Error] In state {} (node_id {}) a codeword is not directly followed by code. This is not allowed.\n"
LOG_WINDOW_FINISHED_STATE_TEXT_PROCESSING = \
"[Info] Finished processing state texts, found {} entry, {} during, {} exit instruction blocks\n" 
LOG_WINDOW_TRANSITION_TEXT_PROCESSING_IN_PROGRESS = \
"[Info] Started processing the transition texts\n"
LOG_WINDOW_TRANSITION_HAS_NO_PRIORITY = \
"[Info] Transition with edge_id {} has no explicit priority, assuming 1 (== highest)\n"
LOG_WINDOW_TRANSITION_HAS_WRONG_PRIORITY = \
"[Warning] Transition with edge_id {} has a wrong priority <= 0, assuming 1 (== highest)\n"
LOG_WINDOW_TRANSITION_TEXT_PROCESSING_CONDITION_PROBLEM = \
"[Warning] Problem processing transition with edge_id {}: Something went wrong parsing condition\n\
instructions, will generate without a generation\n"
LOG_WINDOW_TRANSITION_TEXT_PROCESSING_ACTION_PROBLEM = \
"[Warning] Problem processing transition with edge_id {}: Something went wrong parsing action\n\
instructions, will generate without a generation\n"
LOG_WINDOW_FINISHED_TRANSITION_TEXT_PROCESSING = \
"[Info] Finished processing transition texts, found {} with condition,\n\
{} with action and {} without any instruction blocks\n" 
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IN_PROGRESS = \
"[Info] Started processing the confguration texts\n"
LOG_WINDOW_FINISHED_CONFIGURATION_TEXT_PROCESSING = \
"[Info] Finished processing configuration texts, found\n\
{} input signals, {} output signals, {} local variables and {} lines of preprocessor directives\n" 
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_IO_PROBLEM = \
"[Warning] Problem processing input-/output signals configuration text:\n{}\n\
A line should contain a valid datatype and variable name, separated by a space and finished by a semicolon\n"
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_NO_INIT_VALUE = \
"[Warning] Problem processing variables configuration text while searching for \' = \' sign:\n{}\n\
Searching for an intial value for given local variable failed. Variable will be initialized with 0.\n"
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_TO_MUCH_EQUAL_SIGNS = \
"[Warning] Problem processing variables configuration text while searching for \'=\' sign:\n{}\n\
Too much \'=\' signs were found, variable processing will be skipped.\n"
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_NO_SEMICOLON = \
"[Warning] Problem processing variables configuration text while searching for \';\' sign:\n{}\n\
Line\'s last sign should be a semicolon. Variable processing will be skipped.\n"
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_INVALID_DATATYPE = \
"[Warning] Problem processing variables configuration text:\n{}\n\
Datatype processing failed (read datatype: {}). Variable processing will be skipped.\n"
LOG_WINDOW_CONFIGURATION_TEXT_PROCESSING_VARIABLES_INVALID_VARIABLE_NAME_OR_DATATYPE = \
"[Warning] Problem processing variables configuration text:\n{}\n\
Datatype and/or variable name processing failed when\n\
splitting based on space chars.Variable processing will be skipped.\n"
LOG_WINDOW_PATCH_STATE_TEXT_IN_PROGRESS = \
"[Info] Started patching the state texts for appropriate in- and output signal access.\n"
LOG_WINDOW_PATCH_STATE_TEXT_FINISHED = \
"[Info] Finished patching the state texts.\n\
Patched {} states and {} occurences of in- and output signals\n"
LOG_WINDOW_PATCH_TRANSITION_TEXT_IN_PROGRESS = \
"[Info] Started patching the transition texts for appropriate in- and output signal access.\n"
LOG_WINDOW_PATCH_TRANSITION_TEXT_FINISHED = \
"[Info] Finished patching the transition texts.\n\
Patched {} transitions and {} occurences of in- and output signals\n"
LOG_WINDOW_INVOKING_GENERATOR = \
"\n[Info] Preperations finished.\nStarting generation...\n\n"
LOG_WINDOW_GENERATOR_ERROR_OPENING_OUTPUT_FILE = \
"[Error] Problem opening output file: {}\n"
LOG_WINDOW_GENERATOR_PROBLEM_OPENING_HEADER_TEMPLATE_FILE = \
"[Warning] Problem opening header template file, skipping file header generation:\n\
{}\n"
LOG_WINDOW_GENERATOR_SOURCE_STATE_OF_TRANSITION_NOT_FOUND = \
"[Warning] Couldn\'t find the source state of transition with edge_id {}, skip this transition\n"
LOG_WINDOW_GENERATOR_DESTINATION_STATE_OF_TRANSITION_NOT_FOUND = \
"[Warning] Couldn\'t find the destination state of transition with edge_id {}, skip this transition\n"
LOG_WINDOW_GENERATOR_TRANSITIONS_HAVE_SAME_PRIORITY = \
"[Warning] Some transitions connected to source state node_id {} (state name {})\n\
have the same priority <{}>. This may leads to undefined behaviour!\n"
LOG_WINDOW_GENERATION_STATS = \
"\n\
Files generated:\n\
{} ({})\n\
{}  ({}).\n\
There were {} warnings and {} errors.\n"
DEBUG_HEADER_START = \
    '****************************************** BEGIN DEBUG INFORMATION *******************************************\n'
DEBUG_HEADER_STOP = \
    '******************************************* END DEBUG INFORMATION ********************************************\n'
