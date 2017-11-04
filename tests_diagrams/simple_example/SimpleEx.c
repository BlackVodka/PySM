/******************************************************************************
 *                                                                            *
 * Generated by pySM - The python state machine code generator                *
 *                                                                            *
 *****************************************************************************/

/**
 * @file SimpleEx.c
 * @author Markus Burger
 * @date 2017-11-04
 * @brief Header for generated state machine simpleEx
 * Generated 2017-11-04 13:36:42 by PySM - The python state machine generator.
 */
 

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */
#include "SimpleEx.h"


/* ========================================================================= */
/* STATE FUNCTION (SF) PROTOTYPES                                            */
/* ========================================================================= */
static void simpleEx_SF_state1_entry(void);
static void simpleEx_SF_state2_entry(void);
static void simpleEx_SF_state2(void);
static void simpleEx_SF_state3_entry(void);
static void simpleEx_SF_state3_exit(void);


/* ========================================================================= */
/* STATE MACHINE VARIABLE RESET FUNCTION                                     */
/* ========================================================================= */
static void simpleEx_variableResetFunction(void);


/* ========================================================================= */
/* CREATION OF STATE OBJECTS                                                 */
/* ========================================================================= */
static const pySm_stateType simpleEx_state_state1 =
{
		.onEntryState = simpleEx_SF_state1_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR
};

static const pySm_stateType simpleEx_state_state2 =
{
		.onEntryState = simpleEx_SF_state2_entry,
		.onState = simpleEx_SF_state2,
		.onExitState = PYSM_NULL_PTR
};

static const pySm_stateType simpleEx_state_state3 =
{
		.onEntryState = simpleEx_SF_state3_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = simpleEx_SF_state3_exit
};


/* ========================================================================= */
/* CREATION OF STATE OBJECT POINTER ARRAY                                    */
/* ========================================================================= */
static const pySm_stateType* simpleEx_states_pa[3] =
{
		&simpleEx_state_state1,
		&simpleEx_state_state2,
		&simpleEx_state_state3
};


/* ========================================================================= */
/* CREATION OF STATE TRANSITIONS ARRAY                                       */
/* ========================================================================= */
static pySm_stateTransitionType simpleEx_transitions_sa[3] = 
{
	{
		&simpleEx_state_state1,
		&simpleEx_state_state2,
		PYSM_NULL_PTR,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&simpleEx_state_state2,
		&simpleEx_state_state3,
		PYSM_NULL_PTR,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&simpleEx_state_state3,
		&simpleEx_state_state1,
		PYSM_NULL_PTR,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	}
};


/* ========================================================================= */
/* CREATION OF STATE MACHINE OBJECT                                          */
/* ========================================================================= */
pySm_stateMachineType simpleEx_stateMachine_s = 
{
	&simpleEx_state_state1,
	&simpleEx_state_state1,
	simpleEx_states_pa,
	3u,
	simpleEx_transitions_sa,
	3u,
	PYSM_TRUE,
	simpleEx_variableResetFunction
};


/* ========================================================================= */
/* DE- AND INITALIZATION OF MODULE LOCAL (STATIC) VARIABLES                  */
/* ========================================================================= */
static simpleEx_activeStateType simpleEx_activeState = SIMPLEEX_UNINITALIZED_STATE_MACHINE;

pySm_uint8 local_variable_ui8 = 0u;


/* ========================================================================= */
/* IMPLEMENTATION : STATE MACHINE VARIABLE RESET FUNCTION                    */
/* ========================================================================= */
static void simpleEx_variableResetFunction(void)
{
	local_variable_ui8 = 0u;
}


/* ========================================================================= */
/* IMPLEMENTATION : STATE FUNCTIONS                                          */
/* ========================================================================= */
static void simpleEx_SF_state1_entry(void)
{
	simpleEx_activeState = SIMPLEEX_state1;
	local_variable_ui8 = 1u;
}

static void simpleEx_SF_state2_entry(void)
{
	simpleEx_activeState = SIMPLEEX_state2;
}

static void simpleEx_SF_state2(void)
{
	local_variable_ui8 = 2u;
}

static void simpleEx_SF_state3_entry(void)
{
	simpleEx_activeState = SIMPLEEX_state3;
}

static void simpleEx_SF_state3_exit(void)
{
	local_variable_ui8 = 3u;
}



/* ========================================================================= */
/* IMPLEMENTATION : API FUNCTIONS                                            */
/* ========================================================================= */
pySm_returnType SimpleEx_mainFunction(void)
{
	pySm_returnType runStateMachineResult;


	runStateMachineResult = PySm_runStateMachine(&simpleEx_stateMachine_s);
	return runStateMachineResult;
}

void SimpleEx_getActiveState(simpleEx_activeStateType* swc_activeState)
{
	*swc_activeState = simpleEx_activeState;
}

