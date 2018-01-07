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
 * @file PySm.c
 * @author Markus Burger
 * @date 2017-09-11
 * @brief File containing the main implementation of the
 * pySM API and internal functions
 */

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */
#include "PySm.h"


/* ========================================================================= */
/* STATIC FUNCTION PROTOTYPES                                                */
/* ========================================================================= */
static pySm_returnType PySm_checkState(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType *stateToCheck );
static pySm_stateTransitionType* PySm_findExitingTransition(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType *currState );
static void PySm_runExitOfSubstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType *stateWithTriggeredExit );
static void PySm_runExitOfSuperstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType *stateWithTriggeredExit,
		const pySm_stateType *targetFinalState);
static void PySm_exitState(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType *stateToExit,
		const pySm_stateType *targetState);
static void PySm_runDuringInstructions(
		const pySm_stateMachineType *stateMachine);
static void PySm_enterState(
		pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateToEnter);


/* ========================================================================= */
/* IMPLEMENTATION OF API FUNCTIONS                                           */
/* ========================================================================= */
pySm_returnType PySm_runStateMachine(pySm_stateMachineType *stateMachine)
{
   pySm_returnType returnValue = PYSM_INVALID_MACHINE;
   const pySm_stateType *stateToTestForExit = stateMachine->actualState;
   pySm_stateTransitionType* exitingTransition = PYSM_NULL_PTR;


   if(stateMachine == PYSM_NULL_PTR)
   {
      returnValue = PYSM_INVALID_MACHINE;
   }
   else
   {
/* Check if state is valid                                                   */
      {
         returnValue = PySm_checkState(stateMachine, stateMachine->actualState);

         if(returnValue == PYSM_E_OK)
         {
/* Check if the state machine runs the first time and we need to run an      */
/* entry function                                                            */
/* if/else statement here is needed to ensure a consistent behavior of the   */
/* state machine (entry-statement gets executed in one cycle and just in the */
/* next the during statement gets executed                                   */
        	 if((pySm_bool)PYSM_TRUE == stateMachine->firstRun)
        	 {
        		 PySm_enterState(stateMachine, stateMachine->states[stateMachine->firstValidStateNo]);
        		 stateMachine->firstRun = (pySm_bool)PYSM_FALSE;
        	 }
        	 else
        	 {
            	 /* Check current active state and superstates (if any) for exiting transitions */
        		 do
        		 {
        			 exitingTransition = PySm_findExitingTransition(stateMachine, stateToTestForExit);
        			 /* Go one level higher in state hierarchy, if any */
        			 if(stateToTestForExit->superstateElementNo >= stateMachine->firstValidStateNo)
        			 {
        				 stateToTestForExit = stateMachine->states[(pySm_uint8)stateToTestForExit->superstateElementNo];
        			 }
        			 else
        			 {
        				 /* topmost level reached */
        				 break;
        			 }
        		 }
        		 while(PYSM_NULL_PTR == exitingTransition);

        		 /* Check if an exit from current active state has been triggered */
        		 if(PYSM_NULL_PTR != exitingTransition)
        		 {
        			 /* Run transition action function, if any */
        			 if(PYSM_NULL_PTR != exitingTransition->transitionAction)
        			 {
        				 exitingTransition->transitionAction();
        			 }
        			 PySm_exitState(stateMachine, stateToTestForExit, exitingTransition->destinationState);
        			 PySm_runDuringInstructions(stateMachine);
        			 PySm_enterState(stateMachine, exitingTransition->destinationState);
        		 }
        		 else
        		 {
        			 /* No exit triggered, run current active states, if a during()-function got generated */
        			 PySm_runDuringInstructions(stateMachine);
        		 }
        	 }
		}
	 }
  }
   return returnValue;
}




pySm_returnType PySm_resetStateMachine(pySm_stateMachineType *stateMachine)
{
   pySm_returnType returnValue = PYSM_INVALID_MACHINE;
   pySm_uint8 stateNo = stateMachine->firstValidStateNo;
   pySm_stateType* statePtr = PYSM_NULL_PTR;


   if(stateMachine == PYSM_NULL_PTR)
   {
      returnValue = PYSM_INVALID_MACHINE;
   }
   else
   {
/* Check entry state validity                                                */
      returnValue = PySm_checkState(stateMachine, stateMachine->entryState);

      if(returnValue == PYSM_E_OK)
      {
/* Reset state machine                                                       */
         stateMachine->actualState = stateMachine->entryState;
/* Reset local, static variables                                             */
         if(PYSM_NULL_PTR != stateMachine->resetVariables)
         {
        	 stateMachine->resetVariables();
         }
/* Reset state status enums */
	for(; stateNo < stateMachine->numberOfStates; stateNo++)
	{
		statePtr = (pySm_stateType*)stateMachine->states[stateNo];
		*(statePtr->stateStatusPtr) = PYSM_STATE_INACTIVE;
	}

         stateMachine->firstRun = (pySm_bool)PYSM_TRUE;

         returnValue = PYSM_E_OK;
      }
   }
   return returnValue;
}



/* ========================================================================= */
/* LOCAL FUNCTIONS                                                           */
/* ========================================================================= */
/**
 * @brief Checks a state of a given state machine
 *
 * Checks, if a given state exists in a given state machine
 * @code
 * pySm_returnType out = pySm_checkState(&stateMachine, &stateToCheck);
 * @endcode
 * @param stateMachine State machine object
 * @param stateToCheck State to check if existing in @p stateMachine
 * @return Returns either PYSM_E_UNKNOWN_STATE when the given state
 * doesn't exist in @p stateMachine or PYSM_E_OK
 */
static pySm_returnType PySm_checkState(const pySm_stateMachineType *stateMachine, const pySm_stateType* stateToCheck)
{
   pySm_returnType returnValue = PYSM_E_UNKNOWN_STATE;
   pySm_uint8 stateCounter;


   for(stateCounter = 0u; stateCounter < stateMachine->numberOfStates; stateCounter++)
   {
      if(stateMachine->states[stateCounter]->onState == stateToCheck->onState)
      {
         returnValue = PYSM_E_OK;
         break;
      }
   }

   return returnValue;
}


static pySm_stateTransitionType* PySm_findExitingTransition(const pySm_stateMachineType *stateMachine, const pySm_stateType* currState)
{
	pySm_uint8 transitionNo_ui8 = 0u;
	pySm_bool transitionTriggered = (pySm_bool)PYSM_FALSE;
	pySm_stateTransitionType* transitionWithTriggeredCondition = PYSM_NULL_PTR;
	pySm_uint8 currentTransitionNo;
	pySm_transitionPriorityType transitionPriority = (pySm_transitionPriorityType)0;
	pySm_uint8 transitionsToTest_aui8[PYSM_MAX_NO_OF_TRANSITIONS_PER_STATE];
	pySm_uint8 numberOfTransitionsToTest_ui8 = 0u;


	/* ========================================================================= */
	/* Check for relevant transitions                                            */
	/* ========================================================================= */
	for(transitionNo_ui8 = 0u; transitionNo_ui8 < stateMachine->numberOfTransitions; transitionNo_ui8++)
	{
	   if(stateMachine->transitions[transitionNo_ui8].sourceState == currState)
	   {
		   transitionsToTest_aui8[numberOfTransitionsToTest_ui8] = transitionNo_ui8;
		   numberOfTransitionsToTest_ui8++;
	   }
	}
	/* ========================================================================= */
	/* Execute relevant transitions                                              */
	/* Naturally, numberOfTransitionsToTest_ui8 is the total amount of           */
	/* transitions exiting the currently active state. We're going use this fact */
	/* ========================================================================= */
	for(transitionPriority = (pySm_transitionPriorityType)1u;
			transitionPriority <= (pySm_transitionPriorityType)numberOfTransitionsToTest_ui8;
			transitionPriority+= (pySm_transitionPriorityType)1)
	{
	/* ========================================================================= */
	/* Search for transition with current checked priority (1,2,3...)            */
	/* ========================================================================= */
		for(transitionNo_ui8=0u; transitionNo_ui8 < numberOfTransitionsToTest_ui8; transitionNo_ui8++)
		{
			currentTransitionNo = transitionsToTest_aui8[transitionNo_ui8];
			if(stateMachine->transitions[currentTransitionNo].transitionPriority == transitionPriority)
			{
	/* ========================================================================= */
	/* Condition-less transitions will always evaluate to true                    */
	/* ========================================================================= */
				if (PYSM_NULL_PTR == stateMachine->transitions[currentTransitionNo].transitionTest)
				{
					transitionTriggered = (pySm_bool)PYSM_TRUE;
				}
				else
				{
					transitionTriggered =	stateMachine->transitions[currentTransitionNo].transitionTest();
				}

				if (transitionTriggered == (pySm_bool)PYSM_TRUE)
				{
					/* Remember which transition evaluated to true for returning */
					transitionWithTriggeredCondition = (pySm_stateTransitionType*)&stateMachine->transitions[currentTransitionNo];
					break;
				}
			}
		}

	/* ========================================================================= */
	/* Abort outer for loop as soon as a transition condition was true           */
	/* ========================================================================= */
		if(PYSM_TRUE == transitionTriggered)
		{
			break;
		}
	}

	return transitionWithTriggeredCondition;
}


static void PySm_runExitOfSubstates(const pySm_stateMachineType *stateMachine, const pySm_stateType* stateWithTriggeredExit)
{
	pySm_stateType *statePtr = (pySm_stateType*)stateMachine->actualState;

	do
	{
		if(PYSM_NULL_PTR != statePtr->onExitState)
		{
			statePtr->onExitState();
		}

		*(statePtr->stateStatusPtr) = PYSM_STATE_INACTIVE;

		if(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
		{
			statePtr = (pySm_stateType*)stateMachine->states[statePtr->superstateElementNo];
		}
	}
	while(statePtr->superstateElementNo != stateWithTriggeredExit->superstateElementNo);
}


static void PySm_runExitOfSuperstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateWithTriggeredExit,
		const pySm_stateType* targetFinalState)
{
	pySm_stateType* statePtr = (pySm_stateType*)stateWithTriggeredExit;

	do
	{
		if(PYSM_NULL_PTR != statePtr->onExitState)
		{
			statePtr->onExitState();
		}

		*(statePtr->stateStatusPtr) = PYSM_STATE_INACTIVE;

		if(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
		{
			statePtr = (pySm_stateType*)stateMachine->states[statePtr->superstateElementNo];
		}
		else /* reached topmost hierarchical level, no more exits to run */
		{
			break;
		}
	}
	while(statePtr->superstateElementNo != targetFinalState->superstateElementNo);
}


static void PySm_exitState(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateToExit,
		const pySm_stateType* targetState)
{
	/* Is the state which's transition is responsible for an exit a superstate? */
	 if(stateToExit->defaultSubstateElementNo >= stateMachine->firstValidStateNo)
	 {
		 PySm_runExitOfSubstates(stateMachine, stateToExit);
	 }
	 /* Run exit() of exited superstates, if any */
	 PySm_runExitOfSuperstates(stateMachine, stateToExit, targetState);
}


static void PySm_runDuringInstructions(const pySm_stateMachineType *stateMachine)
{
	const pySm_stateType* statePtr = stateMachine->actualState;

	/* Run active states, beginning with the current active at lowest hierarchy */
	do{
		if(PYSM_STATE_ACTIVE == *(statePtr->stateStatusPtr))
		{
			if(PYSM_NULL_PTR != statePtr->onState)
			{
				statePtr->onState();
			}
			if(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
			{
				/* State has a valid superstate */
				statePtr = stateMachine->states[statePtr->superstateElementNo];
			}
			else
			{
				/* Topmost level reached */
				break;
			}
		}
		else
		{
			/* There can't be an active superstate over an inactive substate, so */
			/* we can abort during() - handling here */
			break;
		}
	}
	/* Exit condition should not be necessary, but just for being sure */
	while(PYSM_STATE_ACTIVE == *(statePtr->stateStatusPtr));
}


static void PySm_enterState(
		pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateToEnter)
{
	pySm_stateType* statePtr = (pySm_stateType*)stateToEnter;

	/* This outer do-while-loop ensured running and activating superstates of the target state, beginning */
	/* from the topmost down to the target state itself */
	do
	{
		/* This while loop searches for the topmost inactive state, beginning from the transition target state */
		/* Afterwards, it get's activated and the according entry() get's executed */
		while(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
		{
			/* Check if the found superstate is already activated */
			if(PYSM_STATE_INACTIVE == *(stateMachine->states[statePtr->superstateElementNo]->stateStatusPtr))
			{
				statePtr = (pySm_stateType*)stateMachine->states[statePtr->superstateElementNo];
			}
		}

		if(PYSM_STATE_INACTIVE == *(statePtr->stateStatusPtr))
		{
			/* no check for Nullptr needed, as the entry function will be always generated */
			statePtr->onEntryState();
			*(statePtr->stateStatusPtr) = PYSM_STATE_ACTIVE;
		}
	}
	while(statePtr != stateToEnter);

/* =========================================================================
*	Now we'll need to take care of the fact, that the target state
*	also might be a superstate with default substates
* ========================================================================= */
	if(stateToEnter->defaultSubstateElementNo < stateMachine->firstValidStateNo)
	{
		/* Target state isn't a superstate, set as current active state */
		stateMachine->actualState = stateToEnter;
	}
	else
	{
		do
		{
			statePtr = (pySm_stateType*)stateMachine->states[statePtr->defaultSubstateElementNo];
			statePtr->onEntryState();
			*(statePtr->stateStatusPtr) = PYSM_STATE_ACTIVE;
			stateMachine->actualState = statePtr;
		}
		while(statePtr->defaultSubstateElementNo >= stateMachine->firstValidStateNo);
	}
}
