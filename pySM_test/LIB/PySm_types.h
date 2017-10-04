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
 * @file PySm_types.h
 * @author Markus Burger
 * @date 2017-09-11
 * @brief File containing basic data types
 */
#ifndef PYSM_TYPES_H_
#define PYSM_TYPES_H_

/* ========================================================================= */
/* Copied from GCC header stdint.h                                           */
/* ========================================================================= */

typedef signed char              pySm_int8;
typedef short int                pySm_int16;
typedef int                      pySm_int32;
# if __WORDSIZE == 64
typedef long int                 pySm_int64;
# else
__extension__
typedef long long int            pySm_int64;
# endif

/* Unsigned.  */
typedef unsigned char            pySm_uint8;
typedef unsigned short int       pySm_uint16;
typedef unsigned int             pySm_uint32;

#if __WORDSIZE == 64
typedef unsigned long int        pySm_uint64;
#else
__extension__
typedef unsigned long long int   pySm_uint64;
#endif

/* ========================================================================= */
/* Own defines and typedefs                                                  */
/* ========================================================================= */
typedef unsigned char            pySm_bool;

#define PYSM_TRUE                1u
#define PYSM_FALSE               0u
#define PYSM_STD_ON              1u
#define PYSM_STD_OFF             0u
#define PYSM_NULL_PTR            (void *)0

#endif /* PYSM_TYPES_H_ */
