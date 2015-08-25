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



values = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

output = []
out_series = []
out_parallel = []
# print(values)

ratio = int(input("Enter resistive ratio:"))

result = 0
sign = 1
dratio = 0
counter = 0
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
    # Run through the list of values
    for element in values:
        for part in values:
            # Run through each power of 10 of the value, going no higher than the 
            # power of 10 of the ratio.
            for x in range(0, int(ratio/10) + 1) :
                # Calculate the current value we are comparing against. 
                y = part * 10**(x)
                # Check if there is another value in the list that matches the ratio.
                if (y == currratio * element) :
                    # If so append the value to a list, and set the result flag.
                    output.append([element, y])
                    result = 1
                # Also check if there are any series or parallel combinations that will
                # achieve the ratio.
                for z in range(0, int(ratio/10) + 1) :
                    for item in values:
                        # Make the 'second' resistor value an item of the list, to a valid power
                        # of 10. 
                        second = item * 10**(z)
                        # Check if the value works with the other values chosen, in either a series or 
                        # parallel combination. 
                        if (y == currratio * (element + second)) :
                            out_series.append([y, [element, second]])
                            result = 1
                        elif (y == currratio * (second * element/(second + element))) :
                            out_parallel.append([y, [element, second]])
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