#!/usr/bin/env python
# python

# Title: __init__.py 
#
# Author: Andrew Collins
# 
# Description: Outer init file for library.
#
# Non standard libraries used: 

# from decimal import *
from math import *

__all__ = ['resistor_ratio','family_list']

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.5, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
E48 = [1.0, 1.21, 1.47, 1.78, 2.15, 2.61, 3.16, 3.83, 4.64, 5.62, 6.81, 8.25, 1.05, 1.27, 1.54, 1.87, 2.26, 2.74, 3.32, 
        4.02, 4.87, 5.9, 7.15, 8.66, 1.1, 1.33, 1.62, 1.96, 2.37, 2.87, 3.48, 4.22, 5.11, 6.19, 7.5, 9.09, 
        1.15, 1.4, 1.69, 2.05, 2.49, 3.01, 3.65, 4.42, 5.36, 6.49, 7.87, 9.53]
E96 = [1.0, 1.21, 1.47, 1.78, 2.15, 2.61, 3.16, 3.83, 4.64, 5.62, 6.81, 8.25, 1.02, 1.24, 1.5, 1.82, 2.21, 
        2.67, 3.24, 3.92, 4.75, 5.76, 6.98, 8.45, 1.05, 1.27, 1.54, 1.87, 2.26, 2.74, 3.32, 4.02, 4.87, 
        5.9, 7.15, 8.66, 1.07, 1.3, 1.58, 1.91, 2.32, 2.8, 3.4, 4.12, 4.99, 6.04, 7.32, 8.87, 1.1, 1.33, 
        1.62, 1.96, 2.37, 2.87, 3.48, 4.22, 5.11, 6.19, 7.5, 9.09, 1.13, 1.37, 1.65, 2.0, 2.43, 2.94, 
        3.57, 4.32, 5.23, 6.34, 7.68, 9.31, 1.15, 1.4, 1.69, 2.05, 2.49, 3.01, 3.65, 4.42, 5.36, 6.49, 
        7.87, 9.53, 1.18, 1.43, 1.74, 2.1, 2.55, 3.09, 3.74, 4.53, 5.49, 6.65, 8.06, 9.76]


family_list = {"e12": E12, "E12": E12, "e24": E24, "E24": E24, "e48": E48, "E48": E48, "e96": E96,"E96": E96}

def resistor_ratio(family, ratio, first_val) :
    # Check if requested family exists
    if ((family in family_list) and ratio > 0.0) :
        # Load in values, and init lists
        values = family_list[family]
        output = []
        out_series = []
        out_parallel = []
        # Calculate highest power of 10 (+1) that the values can get to
        pow_high = int(round((log10(ratio * first_val)), 1)) + 1
        # Run through the list of values
        for part in values:
            # Run through each power of 10 of the value, going no higher than the 
            # power of 10 of the ratio.
            for x in range(0, pow_high) :
                # Calculate the current value we are comparing against. 
                y = round((part * 10**(x)), 2)
                # Check if there is another value in the list that matches the ratio.
                if (first_val == ratio* y) :
                    # If so append the value to a list, and set the result flag.
                    output.append([first_val, y])
                    result = 1
                # Also check if there are any series or parallel combinations that will
                # achieve the ratio.
                for z in range(0, pow_high) :
                    for item in values:
                        # Make the 'second' resistor value an item of the list, to a valid power
                        # of 10. 
                        second = round((item * 10**(z)), 2)
                        # Check if the value works with the other values chosen, in either a series or 
                        # parallel combination. 
                        if (first_val == ratio * (y + second)):
                            out_series.append([first_val, [y, second]])
                            result = 1
                        elif (first_val == ratio * (second * y)/(second + y)):
                            out_parallel.append([first_val, [y, second]])
                            result = 1
    elif (ratio < 0.0) :
        print ("Invalid ratio (must be > 0.0)")
        return()
    else :
        print("Invalid family of values.")
        return()

    return (output, out_series, out_parallel)


# if __name__ == "__main__" :
#     import sys 
#     # print (sys.argv)

#     if (len(sys.argv) > 4) :
#         print("Wrong number of arguments")
#     else :
#         family = sys.argv[1]
#         ratio = float(sys.argv[2])
#         val = float(sys.argv[3])
#         c = resistor_ratio(family, ratio, val)
#         print(c)


