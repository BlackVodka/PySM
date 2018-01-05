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


/* ========================================================================= */
/* IMPLEMENTATION OF API FUNCTIONS                                           */
/* ========================================================================= */
pySm_returnType PySm_runStateMachine(pySm_stateMachineType *stateMachine)
{
   pySm_returnType returnValue = PYSM_INVALID_MACHINE;
   pySm_uint8 transitionNo_ui8 = 0u;
   pySm_uint8 currentTransition_ui8 = 0u;
   pySm_bool transitionTriggered_b = (pySm_bool)PYSM_FALSE;
   pySm_transitionPriorityType transitionPriority = (pySm_transitionPriorityType)0;
   pySm_uint8 transitionsToTest_aui8[PYSM_MAX_NO_OF_TRANSITIONS_PER_STATE];
   pySm_uint8 numberOfTransitionsToTest_ui8 = 0u;
   pySm_bool transitionHasBeenExecuted_b = (pySm_bool)PYSM_FALSE;


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
        	 if((pySm_bool)PYSM_TRUE == stateMachine->runEntryOfInitialState_b)
        	 {
        		 stateMachine->actualState->onEntryState();
        		 stateMachine->runEntryOfInitialState_b = (pySm_bool)PYSM_FALSE;
        	 }
        	 else
        	 {
/* Run current active state, if a during()-function got generated            */
				if(PYSM_NULL_PTR != stateMachine->actualState->onState)
				{
					stateMachine->actualState->onState();
				}
        	 }
/* ========================================================================= */
/* Check for relevant transitions                                            */
/* ========================================================================= */
            for(transitionNo_ui8 = 0u; transitionNo_ui8 < stateMachine->numberOfTransitions; transitionNo_ui8++)
            {
               if(stateMachine->transitions[transitionNo_ui8].sourceState->onState == stateMachine->actualState->onState)
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
            		currentTransition_ui8 = transitionsToTest_aui8[transitionNo_ui8];
            		if(stateMachine->transitions[currentTransition_ui8].transitionPriority == transitionPriority)
					{
/* ========================================================================= */
/* Conditionless transitions will always evaluate to true                    */
/* ========================================================================= */
            			if (PYSM_NULL_PTR == stateMachine->transitions[currentTransition_ui8].transitionTest)
            			{
            				transitionTriggered_b = (pySm_bool)PYSM_TRUE;
            			}
            			else
						{
            				transitionTriggered_b =	stateMachine->transitions[currentTransition_ui8].transitionTest();
						}

						if (transitionTriggered_b == (pySm_bool)PYSM_TRUE)
						{
							/* Check if need to run an exit state function   */
							if(PYSM_NULL_PTR != stateMachine->actualState->onExitState)
							{
								stateMachine->actualState->onExitState();
							}
							/* Check if need to run an transition            */
							/* action function                               */
							if(PYSM_NULL_PTR != stateMachine->transitions[currentTransition_ui8].transitionAction)
							{
								stateMachine->transitions[currentTransition_ui8].transitionAction();
							}
							stateMachine->actualState =	stateMachine->transitions[currentTransition_ui8].destinationState;
							/* Check if need to run an entry state function  */
							/* for the new state                             */
							if(PYSM_NULL_PTR != stateMachine->actualState->onEntryState)
							{
								stateMachine->actualState->onEntryState();
							}
/* Set flag for aborting outer transition iteration for-loop                 */
							transitionHasBeenExecuted_b = PYSM_TRUE;
							break;
						}
					}
				}

/* ========================================================================= */
/* Abort outer for loop as soon as a transition condition was true           */
/* ========================================================================= */
            	if(PYSM_TRUE == transitionHasBeenExecuted_b)
            	{
            		break;
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
         stateMachine->runEntryOfInitialState_b = (pySm_bool)PYSM_TRUE;
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
