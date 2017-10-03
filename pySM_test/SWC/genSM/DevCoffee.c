/******************************************************************************
 *                                                                            *
 * Generated by pySM - The python state machine code generator                *
 *                                                                            *
 *****************************************************************************/

/**
 * @file DevCoffee.c
 * @author Markus Burger
 * @date 2017-10-01
 * @brief Header for generated state machine devCoffee
 * Generated 2017-10-01 16:18:02 by PySM - The python state machine generator.
 */
 

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */
#include "DevCoffee.h"


/* ========================================================================= */
/* STATE FUNCTION (SF) PROTOTYPES                                            */
/* ========================================================================= */
static void devCoffee_SF_BREAKFAST_entry(void);
static void devCoffee_SF_BREAKFAST(void);
static void devCoffee_SF_BREAKFAST_exit(void);
static void devCoffee_SF_IN_OFFICE_entry(void);
static void devCoffee_SF_IN_OFFICE(void);
static void devCoffee_SF_GET_COFFEE_entry(void);
static void devCoffee_SF_RELAX_AND_SLEEP_entry(void);
static void devCoffee_SF_RELAX_AND_SLEEP(void);
static void devCoffee_SF_DEVELOPER_IS_ILL_entry(void);
static void devCoffee_SF_DEVELOPER_IS_ILL(void);


/* ========================================================================= */
/* STATE MACHINE VARIABLE RESET FUNCTION                                     */
/* ========================================================================= */
static void devCoffee_variableResetFunction(void);


/* ========================================================================= */
/* STATE TRANSITION TEST FUNCTION (TTF) PROTOTYPES                           */
/* ========================================================================= */
static pySm_bool devCoffee_TTF_IN_OFFICE_to_IN_OFFICE(void);
static pySm_bool devCoffee_TTF_BREAKFAST_to_IN_OFFICE(void);
static pySm_bool devCoffee_TTF_IN_OFFICE_to_GET_COFFEE(void);
static pySm_bool devCoffee_TTF_IN_OFFICE_to_RELAX_AND_SLEEP(void);
static pySm_bool devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_1(void);
static pySm_bool devCoffee_TTF_BREAKFAST_to_DEVELOPER_IS_ILL(void);
static pySm_bool devCoffee_TTF_DEVELOPER_IS_ILL_to_BREAKFAST(void);
static pySm_bool devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_2(void);


/* ========================================================================= */
/* STATE TRANSITION ACTION FUNCTION (TAF) PROTOTYPES                         */
/* ========================================================================= */
static void devCoffee_TAF_IN_OFFICE_to_IN_OFFICE(void);
static void devCoffee_TAF_GET_COFFEE_to_IN_OFFICE(void);
static void devCoffee_TAF_IN_OFFICE_to_RELAX_AND_SLEEP(void);
static void devCoffee_TAF_RELAX_AND_SLEEP_to_BREAKFAST(void);


/* ========================================================================= */
/* CREATION OF STATE OBJECTS                                                 */
/* ========================================================================= */
static const pySm_stateType devCoffee_state_BREAKFAST =
{
		.onEntryState = devCoffee_SF_BREAKFAST_entry,
		.onState = devCoffee_SF_BREAKFAST,
		.onExitState = devCoffee_SF_BREAKFAST_exit
};

static const pySm_stateType devCoffee_state_IN_OFFICE =
{
		.onEntryState = devCoffee_SF_IN_OFFICE_entry,
		.onState = devCoffee_SF_IN_OFFICE,
		.onExitState = PYSM_NULL_PTR
};

static const pySm_stateType devCoffee_state_GET_COFFEE =
{
		.onEntryState = devCoffee_SF_GET_COFFEE_entry,
		.onState = PYSM_NULL_PTR,
		.onExitState = PYSM_NULL_PTR
};

static const pySm_stateType devCoffee_state_RELAX_AND_SLEEP =
{
		.onEntryState = devCoffee_SF_RELAX_AND_SLEEP_entry,
		.onState = devCoffee_SF_RELAX_AND_SLEEP,
		.onExitState = PYSM_NULL_PTR
};

static const pySm_stateType devCoffee_state_DEVELOPER_IS_ILL =
{
		.onEntryState = devCoffee_SF_DEVELOPER_IS_ILL_entry,
		.onState = devCoffee_SF_DEVELOPER_IS_ILL,
		.onExitState = PYSM_NULL_PTR
};


/* ========================================================================= */
/* CREATION OF STATE OBJECT POINTER ARRAY                                    */
/* ========================================================================= */
static const pySm_stateType* devCoffee_states_pa[5] =
{
		&devCoffee_state_BREAKFAST,
		&devCoffee_state_IN_OFFICE,
		&devCoffee_state_GET_COFFEE,
		&devCoffee_state_RELAX_AND_SLEEP,
		&devCoffee_state_DEVELOPER_IS_ILL
};


/* ========================================================================= */
/* CREATION OF STATE TRANSITIONS ARRAY                                       */
/* ========================================================================= */
static pySm_stateTransitionType devCoffee_transitions_sa[9] = 
{
	{
		&devCoffee_state_IN_OFFICE,
		&devCoffee_state_IN_OFFICE,
		devCoffee_TTF_IN_OFFICE_to_IN_OFFICE,
		(pySm_transitionPriorityType)3u,
		devCoffee_TAF_IN_OFFICE_to_IN_OFFICE
	},
	{
		&devCoffee_state_BREAKFAST,
		&devCoffee_state_IN_OFFICE,
		devCoffee_TTF_BREAKFAST_to_IN_OFFICE,
		(pySm_transitionPriorityType)2u,
		PYSM_NULL_PTR
	},
	{
		&devCoffee_state_IN_OFFICE,
		&devCoffee_state_GET_COFFEE,
		devCoffee_TTF_IN_OFFICE_to_GET_COFFEE,
		(pySm_transitionPriorityType)2u,
		PYSM_NULL_PTR
	},
	{
		&devCoffee_state_GET_COFFEE,
		&devCoffee_state_IN_OFFICE,
		PYSM_NULL_PTR,
		(pySm_transitionPriorityType)1u,
		devCoffee_TAF_GET_COFFEE_to_IN_OFFICE
	},
	{
		&devCoffee_state_IN_OFFICE,
		&devCoffee_state_RELAX_AND_SLEEP,
		devCoffee_TTF_IN_OFFICE_to_RELAX_AND_SLEEP,
		(pySm_transitionPriorityType)1u,
		devCoffee_TAF_IN_OFFICE_to_RELAX_AND_SLEEP
	},
	{
		&devCoffee_state_RELAX_AND_SLEEP,
		&devCoffee_state_BREAKFAST,
		devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_1,
		(pySm_transitionPriorityType)2u,
		devCoffee_TAF_RELAX_AND_SLEEP_to_BREAKFAST
	},
	{
		&devCoffee_state_BREAKFAST,
		&devCoffee_state_DEVELOPER_IS_ILL,
		devCoffee_TTF_BREAKFAST_to_DEVELOPER_IS_ILL,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&devCoffee_state_DEVELOPER_IS_ILL,
		&devCoffee_state_BREAKFAST,
		devCoffee_TTF_DEVELOPER_IS_ILL_to_BREAKFAST,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	},
	{
		&devCoffee_state_RELAX_AND_SLEEP,
		&devCoffee_state_BREAKFAST,
		devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_2,
		(pySm_transitionPriorityType)1u,
		PYSM_NULL_PTR
	}
};


/* ========================================================================= */
/* CREATION OF STATE MACHINE OBJECT                                          */
/* ========================================================================= */
pySm_stateMachineType devCoffee_stateMachine_s = 
{
	&devCoffee_state_RELAX_AND_SLEEP,
	&devCoffee_state_RELAX_AND_SLEEP,
	devCoffee_states_pa,
	5u,
	devCoffee_transitions_sa,
	9u,
	PYSM_TRUE,
	devCoffee_variableResetFunction
};


/* ========================================================================= */
/* DE- AND INITALIZATION OF MODULE LOCAL (STATIC) VARIABLES                  */
/* ========================================================================= */
static devCoffee_inputSignalsType* devCoffee_inputSignals;
static devCoffee_outputSignalsType* devCoffee_outputSignals;
static devCoffee_activeStateType devCoffee_activeState = devCoffee_UNINITALIZED_STATE_MACHINE;

pySm_uint8 coffeein_level_ui8 = 0u;
pySm_uint8 productivity_ui8 = 0u;
pySm_uint8 current_hour_ui8 = 0u;


/* ========================================================================= */
/* IMPLEMENTATION : STATE MACHINE VARIABLE RESET FUNCTION                    */
/* ========================================================================= */
static void devCoffee_variableResetFunction(void)
{
	coffeein_level_ui8 = 0u;
	productivity_ui8 = 0u;
	current_hour_ui8 = 0u;
}


/* ========================================================================= */
/* IMPLEMENTATION : STATE FUNCTIONS                                          */
/* ========================================================================= */
static void devCoffee_SF_BREAKFAST_entry(void)
{
	devCoffee_activeState = DEVCOFFEE_BREAKFAST;
	coffeein_level_ui8 = 99u;
}

static void devCoffee_SF_BREAKFAST(void)
{
	coffeein_level_ui8++;
}

static void devCoffee_SF_BREAKFAST_exit(void)
{
	productivity_ui8 = 100u;
}

static void devCoffee_SF_IN_OFFICE_entry(void)
{
	devCoffee_activeState = DEVCOFFEE_IN_OFFICE;
}

static void devCoffee_SF_IN_OFFICE(void)
{
	devCoffee_outputSignals->developer_is_productive_HA_b = PYSM_TRUE;
	current_hour_ui8++;
	coffeein_level_ui8 -= 25;
}

static void devCoffee_SF_GET_COFFEE_entry(void)
{
	devCoffee_activeState = DEVCOFFEE_GET_COFFEE;
	coffeein_level_ui8 = 100u;
	devCoffee_outputSignals->developer_is_productive_HA_b = PYSM_FALSE;
}

static void devCoffee_SF_RELAX_AND_SLEEP_entry(void)
{
	devCoffee_activeState = DEVCOFFEE_RELAX_AND_SLEEP;
	devCoffee_outputSignals->developer_is_productive_HA_b = PYSM_FALSE;
}

static void devCoffee_SF_RELAX_AND_SLEEP(void)
{
	current_hour_ui8++;
	if(current_hour_ui8 >= 24)
	{
	    current_hour_ui8 -= 24;
	}
}

static void devCoffee_SF_DEVELOPER_IS_ILL_entry(void)
{
	devCoffee_activeState = DEVCOFFEE_DEVELOPER_IS_ILL;
}

static void devCoffee_SF_DEVELOPER_IS_ILL(void)
{
	coffeein_level_ui8 = 0u;
	productivity_ui8 = 0u;
	devCoffee_outputSignals->developer_is_productive_HA_b = PYSM_FALSE;
}



/* ========================================================================= */
/* IMPLEMENTATION : TRANSITION TEST FUNCTIONS (TTFs)                         */
/* ========================================================================= */
static pySm_bool devCoffee_TTF_IN_OFFICE_to_IN_OFFICE(void)
{
	pySm_bool rtrn = (
		productivity_ui8 > (pySm_uint8)0u
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_BREAKFAST_to_IN_OFFICE(void)
{
	pySm_bool rtrn = (
		coffeein_level_ui8 >= 100u
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_IN_OFFICE_to_GET_COFFEE(void)
{
	pySm_bool rtrn = (
		coffeein_level_ui8 == 0u
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_IN_OFFICE_to_RELAX_AND_SLEEP(void)
{
	pySm_bool rtrn = (
		current_hour_ui8 >= GO_HOME_TIME
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_1(void)
{
	pySm_bool rtrn = (
		current_hour_ui8 >= WAKE_UP_TIME_H
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_BREAKFAST_to_DEVELOPER_IS_ILL(void)
{
	pySm_bool rtrn = (
		devCoffee_inputSignals->developer_is_ill_HA_b == PYSM_TRUE
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_DEVELOPER_IS_ILL_to_BREAKFAST(void)
{
	pySm_bool rtrn = (
		devCoffee_inputSignals->developer_is_ill_HA_b == PYSM_FALSE
		);
	return rtrn;
}

static pySm_bool devCoffee_TTF_RELAX_AND_SLEEP_to_BREAKFAST_2(void)
{
	pySm_bool rtrn = (
		devCoffee_inputSignals->another_input_ui8 == 42u
		);
	return rtrn;
}


/* ========================================================================= */
/* IMPLEMENTATION : TRANSITION ACTION FUNCTIONS (TAFs)                       */
/* ========================================================================= */
static void devCoffee_TAF_IN_OFFICE_to_IN_OFFICE(void)
{
	productivity_ui8--;
}

static void devCoffee_TAF_GET_COFFEE_to_IN_OFFICE(void)
{
	current_hour_ui8++;
	productivity_ui8 = 100u;
}

static void devCoffee_TAF_IN_OFFICE_to_RELAX_AND_SLEEP(void)
{
	productivity_ui8 = 0u;
}

static void devCoffee_TAF_RELAX_AND_SLEEP_to_BREAKFAST(void)
{
	coffeein_level_ui8 = 0u;
}



/* ========================================================================= */
/* IMPLEMENTATION : API FUNCTIONS                                            */
/* ========================================================================= */
pySm_returnType DevCoffee_mainFunction(devCoffee_inputSignalsType* swc_inputSignals,
		devCoffee_outputSignalsType* swc_outputSignals)
{
	pySm_returnType runStateMachineResult;

	devCoffee_inputSignals = swc_inputSignals;
	devCoffee_outputSignals = swc_outputSignals;

	runStateMachineResult = PySm_runStateMachine(&devCoffee_stateMachine_s);
	return runStateMachineResult;
}

void DevCoffee_getActiveState(devCoffee_activeStateType* swc_activeState)
{
	*swc_activeState = devCoffee_activeState;
}

