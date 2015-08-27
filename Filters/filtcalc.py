#!/usr/bin/env python
# python

import math *
from ..Resistors.resistor_vals import *

# Receive cap values from user in nano-farads
capstr = input("Please enter available capacitor values in nF (space separated): ")

# Receive resistor family string
family_str = input("Please enter the IEC family of resistors: ")

# Split these values into a list of integers
c = map(int, capstr.split(' '))

# Get the desired cutoff frequency in Hz
fc = int(input("Please enter cutoff frequency (Hz): "))

# Generate the valid list of resistor values 
R = []
print ("Valid resistor values are: ")
for element in c :
    x = 1/(fc * element * 2 * pi * 10**(-9))
    # print(element, "nF -> ", int(x), "Ohms")
    R.append(x)

for element in R :
    temp = resistor_ratio(family_str, 1, element)
    if ()
