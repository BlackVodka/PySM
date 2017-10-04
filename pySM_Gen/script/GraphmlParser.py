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

"""Parses a given yEd graphml file.

    Parses a given yEd graphml file, getting informations like
    contained states, transitions and configuration blocks.
    Other objects will be ignored.
    """

from script import Template_strings as TS
import xml.etree.ElementTree as ET


# XML Namespaces
xmlns = {
    "default" : "{http://graphml.graphdrawing.org/xmlns}",
    "java" : "{http://www.yworks.com/xml/yfiles-common/1.0/java}",
    "sys" : "{http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0}",
    "x" : "{http://www.yworks.com/xml/yfiles-common/markup/2.0}",
    "xsi" : "{http://www.w3.org/2001/XMLSchema-instance}",
    "y" : "{http://www.yworks.com/xml/graphml}",
    "yed" : "{http://www.yworks.com/xml/yed/3}",
    "schemaLocation" : "{http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd}"
    }

# definition of object types, should not be changed because of
# hardcoded sub-types, e.g. GenericNode
state_xml_object = "com.yworks.flowchart.process"
initMarker_xml_object = "com.yworks.flowchart.start2"
configBlock_xml_object = "com.yworks.flowchart.predefinedProcess"

# keywords in states
list_of_keywords = ['entry', 'during', 'exit']

# config block keywords
cfgKw_variables = 'VARIABLES'
cfgKw_defines = 'PREPROCESSOR_DIRECTIVES'
cfgKw_inSigs = 'INPUT_SIGNALS'
cfgKw_outSigs = 'OUTPUT_SIGNALS'


def ParseGraphmlFile(self):
    """Main routine for parsing a yEd graphml file.

    Gets information of contained states, transitions and configuration blocks.
    After trying to open the (GUI-)given input file, it it parses the
    graphml file with the python module xml.etree.ElementTree.
    afterwards, parsing of the needed objects is done in subfuctions.
    After the parsing has been finished, the initialState-attribute
    of the init state is set.

    Args:
        self.txtPathToyEDInputFile: Given yEd graphml file

    Returns:
        Either None, if an error in the parsing subfunctions happened or
        a tupel containing dicts
        parsedStates, parsedConfig, parsedTransitions.
        Each dict's entries will be described in the according parsing
        subfunctions.
    """

    # check if given file can be opened
    try:
        fp = open(self.txtPathToyEDInputFile.text(), 'r')
    except:
        self.logWindow(TS.LOG_WINDOW_ERROR_OPENING_YED_INPUT_FILE)
        return None
    
    self.logWindow(TS.LOG_WINDOW_PARSING_IN_PROGRESS.format(self.txtPathToyEDInputFile.text()))
    tree = ET.parse(fp)
    root = tree.getroot()
    fp.close()
    

    graph = root.findall(xmlns['default'] + 'graph')
    if graph is not None:
        nodes = graph[0].findall(xmlns['default'] + 'node')
        edges = graph[0].findall(xmlns['default'] + 'edge')
        if (edges is None) or (nodes is None):
            return None
    else:
        return None
    
# Catch return None when an error happened parsing nodes
    try:
        (initStateMarkerNodeId, parsedStates, parsedConfig) = ParseNodes(self, nodes)
    except:
        return None
    
# Catch return None when an error happened parsing edges    
    try:
        (initStateNodeId, parsedTransitions) = ParseEdges(self, edges, initStateMarkerNodeId)
    except:
        return None

    # Check if returned transitions and states are not empty:
    if not parsedStates:
        self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_NO_STATES_FOUND)
        return None
    if not parsedTransitions:
        self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_NO_TRANSITIONS_FOUND)
        return None
    
    # Set init state property
    for state in parsedStates:
        if state['node_id'] == initStateNodeId:
            state['is_init_state'] = True

    return (parsedStates, parsedConfig, parsedTransitions)

def ParseNodes(self, nodes):
    """Parses node elements

    A state is represented by a specific node element
    com.yworks.flowchart.process.
    Also, configuration informations are represented by other specific
    node elements, com.yworks.flowchart.predefinedProcess and
    the initial state is represented by a connected circle element
    called com.yworks.flowchart.start2.
    The found nodes will be searched for containing (initial-,)state
    or configuration representations.
    A lot of basic errors are catched here, like e.g. a state containing no
    title/text.

    Args:
        nodes: Found node elements

    Returns:
        Either None, if an error happened
        or
        a a tuple (initStateMarkerNodeId, parsedStates, parsedConfig).
        initStateMarkerNodeId is the NodeId of the inital state marker,
        parsedStates a list of parsed state dictionarys, containing:
            "node_id" : State's NodeId,
            "state_name" : State's name,
            "list_of_text_lines" : None or State's contained text,
            "is_init_state" : True/False
        parsedConfig is a dictionary, containing:
            "cfgVarLines": None or text of a cfgKw_variables configuration block,
            "cfgPreprocessorLines" : None or text of a cfgKw_defines config block,
            "cfgInSigLines" : None or text of a cfgKw_inSigs config block,
            "cfgOutSigLines" : None or text of a cfgKw_outSigs config block
    """
    
    initStateMarkerNodeId = None
    parsedStates = []
    parsedConfig = {
        "cfgVarLines": None,
        "cfgPreprocessorLines" : None,
        "cfgInSigLines" : None,
        "cfgOutSigLines" : None
        }
    
    for currNode in nodes:
        tempNode = currNode[0].find(xmlns['y'] + 'GenericNode')
        if tempNode is not None:
            # Handle GenericNodes of type: state
            if (tempNode.attrib).get('configuration') == state_xml_object:
                try:
                    lines = ((tempNode.find(xmlns['y'] + 'NodeLabel')).text).split('\n')
                except:
                    self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_NO_STATE_TEXT_FOUND.format((currNode.attrib).get('id')))
                    return None
                # Check if state name was read successfully
                if any(s in lines[0] for s in list_of_keywords):
                    self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_STATE_NAME.format((currNode.attrib).get('id'), lines[0]))
                    return None
                if len(lines) < 2:
                    self.logWindow(TS.LOG_WINDOW_WARNING_STATE_HAS_ONLY_NAME.format((currNode.attrib).get('id'), lines[0]))
                    textToAdd = None
                else:
                    textToAdd = lines[1:]
                stateElem = {
                    "node_id" : (currNode.attrib).get('id'),
                    "state_name" : lines[0],
                    "list_of_text_lines" : textToAdd,
                    "is_init_state" : False
                    }
    
                parsedStates.append(stateElem)
                
                
            # Handle GenericNodes of type: Init state marker
            elif (tempNode.attrib).get('configuration') == initMarker_xml_object:
                initStateMarkerNodeId = (currNode.attrib).get('id')
                

            # Handle GenericNodes of type: Configuration block    
            elif (tempNode.attrib).get('configuration') == configBlock_xml_object:
                lines = ((tempNode.find(xmlns['y'] + 'NodeLabel')).text).split('\n')
                if cfgKw_variables in lines[0]:
                    parsedConfig['cfgVarLines'] = lines[1:]
                elif cfgKw_defines in lines[0]:
                    parsedConfig['cfgPreprocessorLines'] = lines[1:]
                elif cfgKw_inSigs in lines[0]:
                    parsedConfig['cfgInSigLines'] = lines[1:]
                elif cfgKw_outSigs in lines[0]:
                    parsedConfig['cfgOutSigLines'] = lines[1:]
                else:
                    self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_CONFIG_BLOCK.format((currNode.attrib).get('id'), lines[0]))
                    return None

                
    if initStateMarkerNodeId is None:
        self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_NO_INIT_STATE_MARKER)
        return None

    return (initStateMarkerNodeId, parsedStates, parsedConfig)


def ParseEdges(self, edges, initStateMarkerNodeId):
    """Parses edge elements

    A transition is represented by a direct connection between
    two state elements, called edge in the graphml file.

    Args:
        edges: Found edge elements
        initStateMarkerNodeId: NodeId of the inital state marker

    Returns:
        Either None, if an error happened
        or
        a a tuple (initStateNodeId, parsedTransitions).
        initStateNodeId is the NodeId of the inital state marker
        parsedTransitions is a list of parsed transition dicts, containing:
        'edge_id' : EdgeId of the transition
        'sourceNode' : NodeId of the starting node
        'targetNode' : NodeId of the target node
        'transitionTextLines' : None or a list of transition text lines
    """
    initStateNodeId = None
    parsedTransitions = []


    for currEdge in edges:

        try:
            lines = ((((currEdge[0][0]).find(xmlns['y'] + 'EdgeLabel'))).text).split('\n')
        except:
            # Transition hasn't any text
            lines = None

        transitionElem = {
            'edge_id' : (currEdge.attrib)['id'],
            'sourceNode' : (currEdge.attrib)['source'],
            'targetNode' : (currEdge.attrib)['target'],
            'transitionTextLines' : lines
            }
        if transitionElem['sourceNode'] == initStateMarkerNodeId:
            initStateNodeId = transitionElem['targetNode']
        # don't add init state transition to list of transitions
        else:
            parsedTransitions.append(transitionElem)

        
    if initStateNodeId is None:
        self.logWindow(TS.LOG_WINDOW_ERROR_PARSING_INIT_STATE_NOT_FOUND)
        return None

    return (initStateNodeId, parsedTransitions)
