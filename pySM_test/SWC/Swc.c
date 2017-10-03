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
 *   Box is distributed in the hope that it will be useful,                   *
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
#include "Swc.h"

/* Important: Include the header file of the generated state machine         */
#include "DevCoffee.h"
#include "SimpleEx.h"

/* Use your own types here, if you like                                      */
#include <stdint.h>

/* ========================================================================= */
/* IMPLEMENTATION                                                            */
/* ========================================================================= */

void Swc_main(void)
{
/* Creation of the state machine input and output signal structs,            */
/* if necessary                                                              */
	devCoffee_inputSignalsType swc_devCoffeeInputSignals;
	devCoffee_outputSignalsType swc_devCoffeeOutputSignals;
/* If you like to, you can get the current active state                      */
	devCoffee_activeStateType swc_devCoffeeActiveState;
	simpleEx_activeStateType swc_simpleExActiveState;

	uint8_t n = 50;

/* Fill needed input signals with values                                     */
	swc_devCoffeeInputSignals.developer_is_ill_HA_b = (pySm_bool)0u;
	swc_devCoffeeInputSignals.another_input_ui8 = 41u;


/* Run the state machine n times                                             */
	for(; n > 0; n--)
	{
		DevCoffee_mainFunction(&swc_devCoffeeInputSignals, &swc_devCoffeeOutputSignals);
		DevCoffee_getActiveState(&swc_devCoffeeActiveState);
		if(DEVCOFFEE_DEVELOPER_IS_ILL == swc_devCoffeeActiveState)
		{
			asm("nop");
			/* do sth. if developer is ill */
		}
		SimpleEx_mainFunction();
		SimpleEx_getActiveState(&swc_simpleExActiveState);
	}
}
