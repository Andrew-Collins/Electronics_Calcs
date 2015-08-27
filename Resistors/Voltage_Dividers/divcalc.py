#!/usr/bin/env python
# python

# Title: rescalc.py
#
# Author: Andrew Collins
# 
# Description: Basic code to calculate resistor values that match a given ratio from a voltage divider equation. 
#              Looking to do this with more resistor value standards.  
#
# Non-standard libraries used: 

# from resistor_vals import *

from ..resistor_vals import *

__all__ = ['ratio_calc']

def ratio_calc():
    # print(values)

    ratio = int(input("Enter resistive ratio:"))

    result = 0

    while (result == 0) :
        family = input("Enter IEC standard: ")
        if (family in family_list) :
            values = family_list[family]
            result = 1
        else :
            print("Invalid standard")

    result = 0
    sign = 1
    dratio = 0
    counter = 0

    output = []
    out_series = []
    out_parallel = []

    # Loop through each combination of values, and check each one to see if
    # it matches the ratio.
    while (result == 0 and counter < 2) :
        # Check if the deviation from the original ratio is greater than 1 
        if (dratio >= 1.0) :
            # If so reset the change, flip the sign of the change, and increment
            # the counter.
            dratio = 0.0
            sign = -sign
            counter = counter + 1
        # Calculate the current deviation from the original ratio
        change = sign * dratio
        currratio = ratio + change
        for element in values:
            temp = resistor_ratio(family, currratio, element)
            if (len(temp[0]) > 0) :
                output.append(temp[0])
                result = 1
            if (len(temp[1]) > 0) :
                out_series.append(temp[1])
                result = 1
            if (len(temp[2]) > 0) :
                out_parallel.append(temp[2])
                result = 1
        #Increment the change in ratio
        dratio = dratio + 0.01

    print()
    # Check if a result within the range of ratios was found.
    if (result == 1) :
        # If so print the values found.
        print("Ratio: ", ratio + change)
        print()
        print("Normalised standard values: ")
        print()
        print("Both values standard:")
        print(output)
        print("One value is a series combination: ")
        print(out_series)
        print("One value is a parallel combination: ")
        print(out_parallel)


    else : 
        # Otherwise break the bad news.
        print("No matching values.")

