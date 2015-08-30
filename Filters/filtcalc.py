#!/usr/bin/env python
# python


from ..Resistors.resistor_vals import *
from math import * 

__all__ = ['filtcalc']

def filtcalc() :
    # Receive cap values from user in nano-farads
    capstr = input("Please enter available capacitor values in nF (space separated): ")
    
    # Receive resistor family string
    family_str = input("Please enter the IEC family of resistors: ")
    
    # Split these values into a list of integers
    c = map(int, capstr.split(' '))
    # Non-mapped cap array for later
    cp = []
    
    # Get the desired cutoff frequency in Hz
    fc = int(input("Please enter cutoff frequency (Hz): "))
    
     
    RT = []
    vals = []
    print ("Valid resistor values are: ")
    print()
    # Generate the valid list of resistor values
    for element in c :
        cp.append(element)
        result = 0
        k = 0
        # Calculate the float resistor value for 
        #  the current cap
        x = 1/(fc * element * 2 * pi * 10**(-9))
        # Loop until valid result produced, or rounding
        #  is too agressive.
        while (result == 0 and k < 4) :
            # Create empty list to store R values
            R = [[],[],[]]
            # Round this value, amount of rounding 
            #  starts from 4th most significant digit
            #  and progresses up with each unsuccessful 
            # loop.
            y = round(x, -int(log10(x)-(4-k)))
            # Feed into resistor finder function
            temp = resistor_ratio(family_str, 1, y)
            # Loop through the returned items
            j = 0
            found = 0
            for item in temp :
                # If a part of the returned tuple is
                #  populated, then load in the values
                if (len(item)) :
                    # Only take the second part of each
                    #  item, as the first part is the 
                    #  value we fed in.
                    found = 1
                    for part in item :
                        R[j].append(part[1])
                j = j + 1
            # Check if there was values found 
            if (found == 1) :
                # Append the current array, to the total
                #  list of values.
                RT.append(R)
                # Set results flag to stop loop
                result = 1
                # Append the calculated and rounded values
                vals.append([x, y])   
            k = k + 1
    for item in range(0, len(RT)) :
        print("The capacitor value ", cp[item], 
            "nF, produced value ", 
            vals[item][0], " and when rounded to ", 
            vals[item][1], 
            " can be produced by values :")
        print("Single Resistor: ", RT[item][0])
        print("Series Combo : ", RT[item][1])
        print("Parallel Combo : ", RT[item][2])
        print()
        



