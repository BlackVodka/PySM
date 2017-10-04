/******************************************************************************
 * Copyright (C) 2017 by Markus Burger                                        *
 *                                                                            *
 * This file is part of pySM - The python state machine code generator        *
 *                                                                            *
 *   pySM is free software: you can redistribute it and/or modify it          *
 *   under the terms of the GNU Lesser General Public License as published    *
 *   by the Free Software Foundation, either version 3 of the License, or     *
 *   (at your option) any later version.                                      *
 *                                                                            *
 *   PySM is distributed in the hope that it will be useful,                  *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
 *   GNU Lesser General Public License for more details.                      *
 *                                                                            *
 *   You should have received a copy of the GNU Lesser General Public         *
 *   License along with Box.  If not, see <http://www.gnu.org/licenses/>.     *
 *****************************************************************************/

/**
 * @file PySm.h
 * @author Markus Burger
 * @date 2017-09-11
 * @brief File containing typedefs and extern
 * callable function declarations.
 */


#ifndef PYSM_H
#define PYSM_H

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */

#include "PySm_Cfg.h"


/* ========================================================================= */
/* TYPEDEFS                                                                  */
/* ========================================================================= */


/**
 * @brief Return type for the pySM librarie's API functions.
 */
typedef enum
{
   PYSM_E_OK = 0u,
   PYSM_E_UNKNOWN_STATE,
   PYSM_E_UNKNOWN_TRANSITION,
   PYSM_INVALID_MACHINE
} pySm_returnType;


/**
 * @brief Function pointer definition for state functions.
 */
typedef void (*pySm_stateFunction)(void);


/**
 * @brief Function pointer definition for state machine reset functions.
 *
 * This function get's generated and is used to reset state machine
 * local internal static variables.
 * This function normally get's called only when resetting a whole
 * state machine by the according API function.
 */
typedef void (*pySm_stateMachineResetFunction)(void);


/**
 * @brief Function pointer definition for state
 * transition functions.
 *
 * These functions get called (if generated/needed) to
 * perform given actions when a transition gets triggered
 * and executed.
 */
typedef void (*pySm_transitionActionFunction)(void);


/**
 * @brief Function pointer definition for state
 * transition test functions.
 *
 * These functions get called to perform the evaluation
 * of the transition condition.
 */
typedef pySm_bool (*pySm_transitionTestFunction)(void);


/**
 * @brief Type for transition priorities.
 */
typedef pySm_uint8 pySm_transitionPriorityType;


/**
 * @brief Structure defining a state
 *
 * A state is defined by it's
 * - entry function PySm_StateType#onEntryState
 * - during (state main function) PySm_StateType#onState
 * - exit function PySm_StateType#onExitState.
 * Each of these functions can be generated as NULL_PTR, if not needed
 */
typedef struct
{
	const pySm_stateFunction         onEntryState; /**< OnEntryState-function, if needed. */
	const pySm_stateFunction         onState;      /**< OnDuringState-function, if needed. */
	const pySm_stateFunction         onExitState;  /**< OnExitState-function, if needed. */
} pySm_stateType;


/**
 * @brief Structure defining a state transition
 *
 * A state transition is defined by it's
 * - source pySm_stateTransitionType#sourceState and
 * - destination state pySm_stateTransitionType#destinationState ,
 * - it's transition condition pySm_StateTransitionType#transitionTest
 * (given by the transition test function)  ,
 * - the transitions priority pySm_stateTransitionType#transitionPriority
 * - and actions to be performed, if an transition has been triggered,
 * given by the transition action function pySm_stateTransitionType#transitionAction
 */
typedef struct
{
   const pySm_stateType*                 sourceState;
   const pySm_stateType*                 destinationState;
   const pySm_transitionTestFunction     transitionTest;
   const pySm_transitionPriorityType     transitionPriority;
   const pySm_transitionActionFunction   transitionAction;
} pySm_stateTransitionType;


/**
 * @brief Structure defining a state machine
 *
 * A state machine is defined by it's
 * - entry state pySm_stateMachineType#entryState
 * - current active state pySm_stateMachineType#actualState
 * - a list of all states, pySm_stateMachineType#states
 * given by an pointer array, pointing
 * to all states of the generated state machine
 * - the overall number of all states
 * pySm_stateMachineType#numberOfTransitions
 * - all existing transitions of the state machine
 * pySm_stateMachineType#transitions, given
 * by an pointer to an array, containing the transitions
 * - the overall number of transitions pySm_stateMachineType#numberOfTransitions
 * - a flag pySm_stateMachineType#runEntryOfInitialState_b,
 * enabling the execution of the onEntry-function of the first,
 * initial state (entryState).
 * This flag get's generated as TRUE when the entryState has an
 * onEntry statement
 * - a function pySm_stateMachineResetFunction#resetVariables for resetting
 * the state machine's local variables
 */
typedef struct
{
   const pySm_stateType*                entryState;
   pySm_stateType*                      actualState;
   const pySm_stateType*                (*states);
   const pySm_uint8                     numberOfStates;
   const pySm_stateTransitionType       *transitions;
   const pySm_uint8                     numberOfTransitions;
   pySm_bool                            runEntryOfInitialState_b;
   const pySm_stateMachineResetFunction resetVariables;
} pySm_stateMachineType;


/* ========================================================================= */
/* API FUNCTIONS                                                             */
/* ========================================================================= */

/**
 * @brief Runs the given state machine.
 *
 * Executes the given state machine
 * @code
 * pySm_returnType out = pySm_runStateMachine(&stateMachine);
 * @endcode
 * @param stateMachine State machine object to run
 * @return Returns either PYSM_INVALID_MACHINE when an invalid
 * statemachine has been given or PYSM_E_OK
 */
pySm_returnType PySm_runStateMachine(pySm_stateMachineType *stateMachine);


/**
 * @brief Resets the given state machine.
 *
 * Resets the given state machine back to initial state and resets
 * the state machine's local variables back to their initial values
 * @code
 * pySm_returnType out = pySm_resetStateMachine(&stateMachine);
 * @endcode
 * @param stateMachine State machine object to reset
 * @return Returns either PYSM_INVALID_MACHINE when an invalid
 * stateMachine has been given or PYSM_E_OK
 */
pySm_returnType PySm_resetStateMachine(pySm_stateMachineType *stateMachine);


#endif /* #ifndef PYSM_H */
