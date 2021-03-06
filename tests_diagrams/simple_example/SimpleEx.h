/******************************************************************************
 *                                                                            *
 * Generated by pySM - The python state machine code generator                *
 *                                                                            *
 *****************************************************************************/

/**
 * @file SimpleEx.h
 * @author Markus Burger
 * @date 2017-11-04
 * @brief Header for generated state machine simpleEx
 * Generated 2017-11-04 13:36:42 by PySM - The python state machine generator.
 */
 
#ifndef SIMPLEEX_H_
#define SIMPLEEX_H_

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */
#include "PySm_types.h"
#include "PySm.h"


/* ========================================================================= */
/* USER PREPROCESSOR DIRECTIVES                                              */
/* ========================================================================= */


/* ========================================================================= */
/* TYPEDEFS                                                                  */
/* ========================================================================= */
/**
 * @brief Enum for exporting current active state of state machine
 * simpleEx
*/
typedef enum
{
	SIMPLEEX_UNINITALIZED_STATE_MACHINE,
	SIMPLEEX_state1,
	SIMPLEEX_state2,
	SIMPLEEX_state3,
} simpleEx_activeStateType;


/* ========================================================================= */
/* API DECLARATION                                                           */
/* ========================================================================= */
/**
 * @brief Main function of the state machine
 * simpleEx
*/
pySm_returnType SimpleEx_mainFunction(void);


/**
 * @brief Main function of the state machine
 * simpleEx
*/
void SimpleEx_getActiveState(simpleEx_activeStateType*);


#endif /* SIMPLEEX_H_ */
