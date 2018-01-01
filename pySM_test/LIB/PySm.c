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
		const pySm_stateType* stateToCheck );
static pySm_stateTransitionType* PySm_findExitingTransition(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* currState );
static void PySm_runExitOfSubstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateWithTriggeredExit );
static void PySm_runExitOfSuperstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateWithTriggeredExit,
		const pySm_stateType* targetFinalState);


/* ========================================================================= */
/* IMPLEMENTATION OF API FUNCTIONS                                           */
/* ========================================================================= */
pySm_returnType PySm_runStateMachine(pySm_stateMachineType *stateMachine)
{
   pySm_returnType returnValue = PYSM_INVALID_MACHINE;
   pySm_stateType* stateToTestForExit = stateMachine->actualState;
   pySm_stateType* transitionTargetFinalState = PYSM_NULL_PTR;
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
        	 if((pySm_bool)PYSM_TRUE == stateMachine->runEntryOfInitialState)
        	 {
        		 stateMachine->actualState->onEntryState();
        		 stateMachine->runEntryOfInitialState = (pySm_bool)PYSM_FALSE;
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
        			 /* Is the state which's transition is responsible for an exit a superstate? */
        			 if((pySm_bool)PYSM_NO_SUPERSTATE != stateToTestForExit->superStateStatus)
        			 {
        				 PySm_runExitOfSubstates(stateMachine, stateToTestForExit);
        			 }
        			 /* Get the final transition target on lowest hierarchical level */
// TODO       			 transitionTargetFinalState = getTransitionTargetFinalState();
        			 /* Run exit() of exited superstates, if any */
        			 PySm_runExitOfSuperstates(stateMachine, stateToTestForExit, transitionTargetFinalState);
        		 }
        		 else
        		 {
        			 /* No exit triggered, run current active state, if a during()-function got generated */
        			 if(PYSM_NULL_PTR != stateMachine->actualState->onState)
        			 {
						stateMachine->actualState->onState();
        			 }
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
	/* ========================================================================= */
	/* Transition action functions will always be executed first, if any         */
	/* ========================================================================= */
					if(PYSM_NULL_PTR != stateMachine->transitions[currentTransitionNo].transitionAction)
					{
						stateMachine->transitions[currentTransitionNo].transitionAction();
					}
					/* Remember which transition evaluated to true for returning */
					transitionWithTriggeredCondition = &stateMachine->transitions[currentTransitionNo];
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
	pySm_stateType* statePtr = stateMachine->actualState;

	do
	{
		if(PYSM_NULL_PTR != statePtr->onExitState)
		{
			statePtr->onExitState();
		}
		if(statePtr->superStateStatus != PYSM_NO_SUPERSTATE)
		{
			statePtr->superStateStatus = PYSM_SUPERSTATE_INACTIVE;
		}
		if(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
		{
			statePtr = stateMachine->states[statePtr->superstateElementNo];
		}
	}
	while(statePtr->superstateElementNo != stateWithTriggeredExit->superstateElementNo);
}


static void PySm_runExitOfSuperstates(
		const pySm_stateMachineType *stateMachine,
		const pySm_stateType* stateWithTriggeredExit,
		const pySm_stateType* targetFinalState)
{
	pySm_stateType* statePtr = stateWithTriggeredExit;

	do
	{
		if(PYSM_NULL_PTR != statePtr->onExitState)
		{
			statePtr->onExitState();
		}

		if(statePtr->superstateElementNo >= stateMachine->firstValidStateNo)
		{
			statePtr = stateMachine->states[statePtr->superstateElementNo];
		}
		else /* reached topmost hierarchical level, no more exits to run */
		{
			break;
		}
	}
	while(statePtr->superstateElementNo != targetFinalState->superstateElementNo);
}
