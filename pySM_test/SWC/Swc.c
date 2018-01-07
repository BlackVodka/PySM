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
 * @file Swc.c
 * @author Markus Burger
 * @date 2017-09-11
 * @brief Test-SWC to demonstrate the use of the generated state machine
 */
/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */
#include <NestedStates.h>
#include "Swc.h"

/* Important: Include the header file of the generated state machine         */
#include <stdint.h>

/* ========================================================================= */
/* IMPLEMENTATION                                                            */
/* ========================================================================= */

void Swc_main(void)
{
/* Creation of the state machine input and output signal structs,            */
/* if necessary                                                              */
	nestedStates_inputSignalsType swc_nestedStatesInputSignals;
	nestedStates_outputSignalsType swc_nestedStatesOutputSignals;
/* If you like to, you can get the current active state                      */
	nestedStates_activeStateType swc_nestedStatesActiveState;

	uint8_t n = 50;

/* Fill needed input signals with values                                     */
	swc_nestedStatesInputSignals.trigger_a = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_b = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_c = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_d = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_e = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_f = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_g = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_h = (pySm_bool)PYSM_FALSE;
	swc_nestedStatesInputSignals.trigger_i = (pySm_bool)PYSM_FALSE;


/* Run the state machine n times                                             */
	for(; n > 0; n--)
	{
		NestedStates_mainFunction(&swc_nestedStatesInputSignals, &swc_nestedStatesOutputSignals);
		NestedStates_getActiveState(&swc_nestedStatesActiveState);
	}
}
