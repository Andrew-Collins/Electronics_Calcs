#!/usr/bin/env python
# python

# Title: volt_div.py
#
# Author: Andrew Collins
# 
# Description: Basic code to calculate resistor values that match a given ratio from a voltage divider equation. 
#              Looking to do this with more resistor value standards.  
#
# Non-standard libraries used: 

# from resistor_vals import *

from .resistor_vals import family_list, resistor_ratio
from copy import deepcopy

__all__ = ['ratio_calc']

# Function name: ratio_calc
#
# Description: Calculates reistor combination from a certain value of resistors, for a voltage divider ratio. 
#
# Inputs: print_flag (integer) : flag that controls whether the results are printed or not. 
#
# Outputs: output (float list) : list of sucessful single value combinations.
#           out_series (float list) : list of successful series combinations. 
#           out_parallel (float list) : list of successful parallel combinations.
#
def ratio_calc(print_flag = 1, family = 0, ratio = 0):
    # print(values)
    if (ratio == 0) :
        ratio = float(input("Enter resistive ratio:"))
    
    if (family == 0) :
        result = 0

        while (result == 0) :
            family = input("Enter IEC standard: ")
            if (family in family_list) :
                values = family_list[family]
                result = 1
            else :
                print("Invalid standard")
    else :
        if (family in family_list) :
            values = family_list[family]
        else :
            return ([],[],[])

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
                for item in temp[0] :
                    output.append(item)
                result = 1
            if (len(temp[1]) > 0) :
                for item in temp[1] :
                    out_series.append(item)
                result = 1
            if (len(temp[2]) > 0) :
                for item in temp[2] :
                    out_parallel.append(item)
                result = 1
        #Increment the change in ratio
        dratio = dratio + 0.01

    print()
    # Check if a result within the range of ratios was found.
    if (print_flag == 1) :
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

    return (output, out_series, out_parallel, ratio + change)




def ratio_calc_single(family, ratio, complexity):
    output = []
    out_series = []
    out_parallel = []
    res = 0

    if (family in family_list) :
        values = [deepcopy(family_list[family])]
        real_values = [deepcopy(family_list[family])]
    else :
        return ([],[],[])


    # Loop through each combination of values, and check each one to see if
    # it matches the ratio.
    for i in range(complexity) :
        if (res == 0) :
            temp_real_vals = []
            temp_vals = []
            for j in range(len(values[i])):
                if (i == 0) :
                    real_values[i][j] = [real_values[i][j]]
                temp = resistor_ratio(family, ratio, values[i][j])
                if (len(temp[0]) > 0) :
                    res = 1
                    for k in range(len(temp[0])) :
                        temp[0][k][0] = real_values[i][j]
                        output.append(temp[0][k])
                if (len(temp[1]) > 0) :
                    res = 1
                    for k in range(len(temp[1])) :
                        temp[1][k][0] = real_values[i][j]
                        out_series.append(temp[1][k])
                if (len(temp[2]) > 0) :
                    res = 1
                    for k in range(len(temp[2])) :
                        temp[2][k][0] = real_values[i][j]
                        out_parallel.append(temp[2][k])

                for k in range(len(values[0])) :
                    # Add a series resistor
                    temp_combo = deepcopy(real_values[i][j])
                    temp_combo.append(values[0][k])
                    temp_real_vals.append(temp_combo) 
                    temp_vals.append(deepcopy(values[i][j]) + values[0][k])

                    #Add a parallel resistor combo
                    for l in range(i + 1):
                        temp_combo = deepcopy(real_values[i][j])
                        if (type(real_values[i][j][l]) != type([1])) :
                            temp_combo[l] = [temp_combo[l]]
                            temp_total = values[i][j] - real_values[i][j][l]
                        else :
                            inv = 0
                            for m in range(len(temp_combo[l])) :
                                inv += 1/float(temp_combo[l][m])
                            temp_total = values[i][j] - 1/inv
                        temp_combo[l].append(values[0][k])
                        inv = 0
                        for m in range(len(temp_combo[l])) :
                            inv += 1/float(temp_combo[l][m])
                        temp_total += 1/inv

                        temp_real_vals.append(temp_combo) 
                        temp_vals.append(temp_total)

            values.append(temp_vals)
            real_values.append(temp_real_vals)

    return (output, out_series, out_parallel)
