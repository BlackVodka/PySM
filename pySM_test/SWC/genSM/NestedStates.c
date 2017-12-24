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
#include "NestedStates.h"


/* ========================================================================= */
/* STATE FUNCTION (SF) PROTOTYPES                                            */
/* ========================================================================= */
static void nestedStates_SF_SUP_A_entry(void);
static void nestedStates_SF_SUP_B_entry(void);
static void nestedStates_SF_SUP_C_entry(void);
static void nestedStates_SF_SUP_D_entry(void);
static void nestedStates_SF_SUB_A_entry(void);
static void nestedStates_SF_SUB_B_entry(void);
static void nestedStates_SF_SUB_C_entry(void);
static void nestedStates_SF_SUB_D_entry(void);
static void nestedStates_SF_SUB_E_entry(void);
static void nestedStates_SF_SUB_F_entry(void);
static void nestedStates_SF_SUB_A(void);
static void nestedStates_SF_SUB_B(void);
static void nestedStates_SF_SUB_C(void);
static void nestedStates_SF_SUB_D(void);
static void nestedStates_SF_SUB_E(void);
static void nestedStates_SF_SUB_F(void);


/* ========================================================================= */
/* STATE MACHINE VARIABLE RESET FUNCTION                                     */
/* ========================================================================= */
static void nestedStates_variableResetFunction(void);


/* ========================================================================= */
/* STATE TRANSITION TEST FUNCTION (TTF) PROTOTYPES                           */
/* ========================================================================= */
static pySm_bool nestedStates_TTF_SUP_A_to_SUP_C(void);
static pySm_bool nestedStates_TTF_SUB_A_to_SUP_C(void);
static pySm_bool nestedStates_TTF_SUB_A_to_SUB_D(void);
static pySm_bool nestedStates_TTF_SUP_A_to_SUB_E(void);
static pySm_bool nestedStates_TTF_SUB_B_to_SUB_C(void);
static pySm_bool nestedStates_TTF_SUB_A_to_SUB_C(void);
static pySm_bool nestedStates_TTF_SUP_B_to_SUB_D(void);
static pySm_bool nestedStates_TTF_SUB_B_to_SUB_D(void);
static pySm_bool nestedStates_TTF_SUB_C_to_SUB_F(void);


/* ========================================================================= */
/* CREATION OF STATE OBJECTS                                                 */
/* ========================================================================= */
static const pySm_stateType nestedStates_state_SUP_A =
{
		.onEntryState = nestedStates_SF_SUP_A_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_RESERVED_NO_VALID_STATE,
		.isSuperState = PYSM_TRUE
};

static const pySm_stateType nestedStates_state_SUP_B =
{
		.onEntryState = nestedStates_SF_SUP_B_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_A,
		.isSuperState = PYSM_TRUE
};

static const pySm_stateType nestedStates_state_SUP_C =
{
		.onEntryState = nestedStates_SF_SUP_C_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_RESERVED_NO_VALID_STATE,
		.isSuperState = PYSM_TRUE
};

static const pySm_stateType nestedStates_state_SUP_D =
{
		.onEntryState = nestedStates_SF_SUP_D_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_C,
		.isSuperState = PYSM_TRUE
};

static const pySm_stateType nestedStates_state_SUB_A =
{
		.onEntryState = nestedStates_SF_SUB_A_entry,
		.onState = nestedStates_SF_SUB_A,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_B,
		.isSuperState = PYSM_FALSE
};

static const pySm_stateType nestedStates_state_SUB_B =
{
		.onEntryState = nestedStates_SF_SUB_B_entry,
		.onState = nestedStates_SF_SUB_B,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_B,
		.isSuperState = PYSM_FALSE
};

static const pySm_stateType nestedStates_state_SUB_C =
{
		.onEntryState = nestedStates_SF_SUB_C_entry,
		.onState = nestedStates_SF_SUB_C,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_A,
		.isSuperState = PYSM_FALSE
};

static const pySm_stateType nestedStates_state_SUB_D =
{
		.onEntryState = nestedStates_SF_SUB_D_entry,
		.onState = nestedStates_SF_SUB_D,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_D,
		.isSuperState = PYSM_FALSE
};

static const pySm_stateType nestedStates_state_SUB_E =
{
		.onEntryState = nestedStates_SF_SUB_E_entry,
		.onState = nestedStates_SF_SUB_E,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_D,
		.isSuperState = PYSM_FALSE
};

static const pySm_stateType nestedStates_state_SUB_F =
{
		.onEntryState = nestedStates_SF_SUB_F_entry,
		.onState = nestedStates_SF_SUB_F,
		.onExitState = PYSM_NULL_PTR,
		.superstateElementNo = (pySm_int8)NESTEDSTATES_SUP_C,
		.isSuperState = PYSM_FALSE
};


/* ========================================================================= */
/* CREATION OF STATE OBJECT POINTER ARRAY                                    */
/* ========================================================================= */
static const pySm_stateType* nestedStates_states_pa[10] =
{
		&nestedStates_state_SUP_A,
		&nestedStates_state_SUP_B,
		&nestedStates_state_SUP_C,
		&nestedStates_state_SUP_D,
		&nestedStates_state_SUB_A,
		&nestedStates_state_SUB_B,
		&nestedStates_state_SUB_C,
		&nestedStates_state_SUB_D,
		&nestedStates_state_SUB_E,
		&nestedStates_state_SUB_F
};


/* ========================================================================= */
/* CREATION OF STATE TRANSITIONS ARRAY                                       */
/* ========================================================================= */
static pySm_stateTransitionType nestedStates_transitions_sa[9] =
{
	{
		&nestedStates_state_SUP_A,
		&nestedStates_state_SUP_C,
		nestedStates_TTF_SUP_A_to_SUP_C,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_A,
		&nestedStates_state_SUP_C,
		nestedStates_TTF_SUB_A_to_SUP_C,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_A,
		&nestedStates_state_SUB_D,
		nestedStates_TTF_SUB_A_to_SUB_D,
		(pySm_transitionPriorityType)2u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUP_A,
		&nestedStates_state_SUB_E,
		nestedStates_TTF_SUP_A_to_SUB_E,
		(pySm_transitionPriorityType)2u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_B,
		&nestedStates_state_SUB_C,
		nestedStates_TTF_SUB_B_to_SUB_C,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_A,
		&nestedStates_state_SUB_C,
		nestedStates_TTF_SUB_A_to_SUB_C,
		(pySm_transitionPriorityType)3u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUP_B,
		&nestedStates_state_SUB_D,
		nestedStates_TTF_SUP_B_to_SUB_D,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_B,
		&nestedStates_state_SUB_D,
		nestedStates_TTF_SUB_B_to_SUB_D,
		(pySm_transitionPriorityType)2u,
		PYSM_NULL_PTR
	},
	{
		&nestedStates_state_SUB_C,
		&nestedStates_state_SUB_F,
		nestedStates_TTF_SUB_C_to_SUB_F,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	}
};


/* ========================================================================= */
/* CREATION OF STATE MACHINE OBJECT                                          */
/* ========================================================================= */
pySm_stateMachineType nestedStates_stateMachine_s =
{
	&nestedStates_state_SUP_A,
	&nestedStates_state_SUP_A,
	nestedStates_states_pa,
	10u,
	nestedStates_transitions_sa,
	9u,
	PYSM_TRUE,
	nestedStates_variableResetFunction
};


/* ========================================================================= */
/* DE- AND INITALIZATION OF MODULE LOCAL (STATIC) VARIABLES                  */
/* ========================================================================= */
static nestedStates_inputSignalsType* nestedStates_inputSignals;
static nestedStates_outputSignalsType* nestedStates_outputSignals;
static nestedStates_activeStateType nestedStates_activeState = NESTEDSTATES_RESERVED_NO_VALID_STATE;

pySm_uint16 localVar = 0u;


/* ========================================================================= */
/* IMPLEMENTATION : STATE MACHINE VARIABLE RESET FUNCTION                    */
/* ========================================================================= */
static void nestedStates_variableResetFunction(void)
{
	localVar = 0u;
}


/* ========================================================================= */
/* IMPLEMENTATION : STATE FUNCTIONS                                          */
/* ========================================================================= */
static void nestedStates_SF_SUP_A_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUP_A;
	localVar = 0u;
}

static void nestedStates_SF_SUP_B_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUP_B;
	localVar = 0u;
}

static void nestedStates_SF_SUP_C_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUP_C;
	localVar = 0u;
}

static void nestedStates_SF_SUP_D_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUP_D;
	localVar = 0u;
}

static void nestedStates_SF_SUB_A_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_A;
}

static void nestedStates_SF_SUB_B_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_B;
}

static void nestedStates_SF_SUB_C_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_C;
}

static void nestedStates_SF_SUB_D_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_D;
}

static void nestedStates_SF_SUB_E_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_E;
}

static void nestedStates_SF_SUB_F_entry(void)
{
	nestedStates_activeState = NESTEDSTATES_SUB_F;
}

static void nestedStates_SF_SUB_A(void)
{
	localVar++;
}

static void nestedStates_SF_SUB_B(void)
{
	localVar++;
}

static void nestedStates_SF_SUB_C(void)
{
	localVar++;
}

static void nestedStates_SF_SUB_D(void)
{
	localVar++;
}

static void nestedStates_SF_SUB_E(void)
{
	localVar++;
}

static void nestedStates_SF_SUB_F(void)
{
	localVar++;
}


/* ========================================================================= */
/* IMPLEMENTATION : TRANSITION TEST FUNCTIONS (TTFs)                         */
/* ========================================================================= */
static pySm_bool nestedStates_TTF_SUP_A_to_SUP_C(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_a
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_A_to_SUP_C(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_b
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_A_to_SUB_D(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_c
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUP_A_to_SUB_E(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_d
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_B_to_SUB_C(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_e
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_A_to_SUB_C(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_f
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUP_B_to_SUB_D(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_g
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_B_to_SUB_D(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_h
		);
	return rtrn;
}

static pySm_bool nestedStates_TTF_SUB_C_to_SUB_F(void)
{
	pySm_bool rtrn = (
		 nestedStates_inputSignals->trigger_i
		);
	return rtrn;
}


/* ========================================================================= */
/* IMPLEMENTATION : API FUNCTIONS                                            */
/* ========================================================================= */
pySm_returnType NestedStates_mainFunction(nestedStates_inputSignalsType* swc_inputSignals,
		nestedStates_outputSignalsType* swc_outputSignals)
{
	pySm_returnType runStateMachineResult;

	nestedStates_inputSignals = swc_inputSignals;
	nestedStates_outputSignals = swc_outputSignals;

	runStateMachineResult = PySm_runStateMachine(&nestedStates_stateMachine_s);
	return runStateMachineResult;
}


void NestedStates_getActiveState(nestedStates_activeStateType* swc_activeState)
{
	*swc_activeState = nestedStates_activeState;
}
