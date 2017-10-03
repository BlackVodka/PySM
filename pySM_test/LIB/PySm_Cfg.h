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
 * @file PySm_Cfg.h
 * @author Markus Burger
 * @date 2017-09-11
 * @brief File containing configuration of the pySM library.
 *
 */


#ifndef PYSM_CFG_H
#define PYSM_CFG_H

/* ========================================================================= */
/* INCLUDES                                                                  */
/* ========================================================================= */

#include "PySm_types.h"


/* ========================================================================= */
/* DEFINES                                                                   */
/* ========================================================================= */

/** @brief Number of maximum allowed in-/outgoing transitions per state */
#define PYSM_MAX_NO_OF_TRANSITIONS_PER_STATE 10u



#endif /* PYSM_CFG_H_ */
