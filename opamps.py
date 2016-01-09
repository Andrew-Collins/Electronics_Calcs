#!/usr/bin/env python
# python

# Title: opamps.py
#
# Author: Andrew Collins
# 
# Description: Houses functions related to opamp circuits. 
#               Wanting to make it both a library and a script.
#
# Non-standard libraries used: 

from .Resistors.volt_div import ratio_calc
from .Resistors.volt_div import ratio_calc_single
from math import log10
from tkinter import *

# Function name: inverting_amp
#
# Description: Calculates a combination of resistors (either singular, series or parallel), that
#               matches a given amplification ratio as closely as possible.
#
# Inputs: family (string) : label of the resistor family being used. 
#         ratio (float/decimal) : value of the ratio needed. 
#
# Outputs: output (float list) : list of sucessful single value combinations.
#           out_series (float list) : list of successful series combinations. 
#           out_parallel (float list) : list of successful parallel combinations.
#


def inverting_amp(family, ratio) :
    return ratio_calc(print_flag = 0, family = family, ratio =ratio)

# Function name: non_inverting_amp
#
# Description: Calculates a combination of resistors (either singular, series or parallel), that
#               matches a given amplification ratio as closely as possible.
#
# Inputs: family (string) : label of the resistor family being used. 
#         ratio (float/decimal) : value of the ratio needed. 
#
# Outputs: output (float list) : list of sucessful single value combinations.
#           out_series (float list) : list of successful series combinations. 
#           out_parallel (float list) : list of successful parallel combinations.
#
def non_inverting_amp(family, ratio) :
    return ratio_calc(print_flag = 0, family = family, ratio = (ratio - 1))

# Function name: non_inverting_summing_amp
#
# Description: Calculates a combination of resistors (either singular, series or parallel), that
#               creates a n-branch non-inverting summing amplifier, with each branch having a 
#               certain amplification ratio.
#
# Inputs: family (string) : label of the resistor family being used. 
#         ratio (float/decimal list) : values of the ratios needed. 
#         branches (integer) : number of input signals to the summing amplifier (must be > 2)
#
# Outputs: output (float list) : list of sucessful single value combinations.
#           out_series (float list) : list of successful series combinations. 
#           out_parallel (float list) : list of successful parallel combinations.
#
def non_inverting_summing_amp(family, ratio, branches, complexity) :
    def scroll(event) :
        w,h = event.width, event.height
        canvas.config(scrollregion=(0,0,w,h))

    def resize(event) :

        hbar.config(command=canvas.xview)
        vbar.grid(row = 1, column = 0, sticky=W+E+N+S)

    if (branches < 2 or branches != len(ratio)) :
        return 0
    else :
        dratio = 0.0
        res = 0
        sign = 1
        while (res != 1) :
            rf_archive = []
            rf = []
            temp = []
            ratios = []
            branch_vals = []
            ratio_powers = []
            max_power = 0

            for i in range(len(ratio)) :
                temp.append(0)
                if (int(log10(ratio[i])) > max_power) :
                    for j in range(i, 0, -1) :
                        temp[j] = temp[j-1]
                    temp[0] = ratio[i]
                    max_power = int(log10(ratio[i]))
                else :
                    temp[i] = ratio[i]

            ratio = temp
            temp = []

            for i in range(len(ratio)) :
                ratio_powers.append(max_power - int(log10(ratio[i])))

            for i in range(len(ratio)) :
                temp_branch_vals = []
                temp_rf_vals = []
                # inv_ratio = 1/(ratio[i]*(1+dratio))
                ratio_single = ratio[i] + dratio
                # temp.append(ratio_calc_single(family, inv_ratio))
                temp.append(ratio_calc_single(family, ratio_single, complexity))
                if (i == 0) :
                    for j in range(3) :
                        temp_branch_vals.append([])
                        temp_rf_vals.append([])
                        for k in range(len(temp[0][j])) :
                            temp_branch_vals[j].append(temp[0][j][k][1])
                            # if (j == 2) :
                            #     temp_rf_vals.append([temp[0][j][k][1], 'P'])
                            # else :
                            
                            temp_rf_vals[j].append(temp[0][j][k][0])
                else :
                    for j in range(3) :
                        temp_branch_vals.append([])
                        temp_rf_vals.append([])
                        for k in range(len(temp[i][j])) :
                            for power in range(ratio_powers[i] + 1) :
                                if ((temp[i][j][k][0]*10**power) in rf[j]) :
                                    if (j > 0) :
                                        for l in range(len(temp[i][j][k][1])) :
                                            temp[i][j][k][1][l] *= 10**power
                                    else :
                                        temp[i][j][k][1] *= 10**power

                                    for l in range(len(temp[i][j][k][0])) :
                                        if (type(temp[i][j][k][0][l]) != type([1])) :
                                            temp[i][j][k][0][l] *= 10**power
                                        else :
                                            for m in range(len(temp[i][j][k][1][l])) :
                                                temp[i][j][k][0][l][m] *= 10**power    

                                    temp_branch_vals[j].append(temp[i][j][k][1])
                                    # if (j == 2):
                                    #     temp_rf_vals.append([temp[i][j][k][1], 'P'])
                                    # else :    
                                    
                                    temp_rf_vals[j].append(temp[i][j][k][0])

                # ratios.append(temp[i][4])
                rf_archive.append(temp_rf_vals)
                rf = temp_rf_vals
                branch_vals.append(temp_branch_vals)
            print(dratio)
            # print(temp)

            if (len(rf[0]) + len(rf[1]) + len(rf[2]) == 0) :
                if (sign == 1) :
                    sign = -1
                    dratio = -dratio
                else :
                    dratio = -dratio + 0.01 
                    sign = 1

                if (dratio > 0.5) :
                    print("Failed to find combination")
                    return 0
            else :
                res = 1
                temp_rf_vals = []
                # for a in range(3) :
                # for c in range(len(rf)) :
                #     if (rf[c] not in temp_rf_vals):
                #         temp_rf_vals.append(rf[c])

                # rf = temp_rf_vals
                combined = []
                # print("Feedback Values: ")
                # print(ratio_powers)
                # print(rf)
                # print(rf_archive[0])
                # print(rf_archive[1])
                # print()

                # master = Tk()
                # overlord = Tk()
                frame = Tk()

                # overlord.bind("<Configure>", resize)

                # frame=Frame(overlord,width=300,height=300)
                # frame.grid()

                frame.grid_columnconfigure(0, weight=1)
                frame.grid_rowconfigure(0, weight=1)

                canvas = Canvas(frame, width=300, height=300)
                canvas.grid(row = 0, column = 0, sticky = N+E+S+W)

                master = Frame()
                master.bind("<Configure>", scroll)
                canvas.create_window(0,0, anchor=NW, window=master)

                hbar=Scrollbar(frame,orient=HORIZONTAL)
                hbar.grid(row = 1, column = 0, sticky=W+E)
                hbar.config(command=canvas.xview)
                vbar=Scrollbar(frame,orient=VERTICAL)
                vbar.grid(row = 0, column = 1, sticky=W+E+N+S)
                vbar.config(command=canvas.yview)
                canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

                # single_total_max = 0
                # series_total_max = 0
                # parallel_total_max = 0
                count_max = 0

                rf_dict = {}
                count = 0
                for d in range(3) :
                    temp_rf_vals.append([])
                    for e in range(len(rf[d])) :
                        if (str(rf[d][e]) not in rf_dict) :
                            rf_dict[str(rf[d][e])] = count
                            count += 1
                            temp_rf_vals[d].append(rf[d][e])

                rf = temp_rf_vals
                rf_columns = []
                for x in range(3) :
                    rf_columns.append([])
                    for y in range(len(rf[x])) :
                        rf_columns[x].append(0)

                # print("Branch Values: ")
                for a in range(len(ratio)) :
                    temp_branch_vals = []
                    count = 0
                    # print("Branch " + str(a) + ":")
                    temp_rf_columns = []
                    for x in range(3) :
                        temp_rf_columns.append([])
                        for y in range(len(rf[x])) :
                            temp_rf_columns[x].append(0)
                    combined.append([])

                    for b in range(3):
                        combined[a].append([])

                        for c in range(len(rf_archive[a][b])) :
                            # if (rf_archive[a][b] in rf) :
                            
                            # for d in range(b) :
                            #     for e in range(len(rf[b])):
                            #         count += rf_columns[b][e]
                            for f in range(len(rf[b])) :
                                if (rf[b][f] == rf_archive[a][b][c] and [branch_vals[a][b][c], rf[b][f]] not in combined[a][b]):
                                    combined[a][b].append([branch_vals[a][b][c], rf[b][f]])
                                    temp_rf_columns[b][f] += 1
                                    # Label(master, text = branch_vals[a][b][c], padx = 5, pady = 5).grid(row = 3+count)
                                    # temp_branch_vals.append(branch_vals[a][b])
                    #                 count += 1

                    # if (count > count_max) :
                    #     count_max = count
                    count_max = 0
                    for g in range(3):
                        for h in range(len(rf[g])) :
                            if (temp_rf_columns[g][h] > rf_columns[g][h]) :
                                rf_columns[g][h] = temp_rf_columns[g][h]

                            count_max += rf_columns[g][h]

                if (count_max > 50) :
                    rf_title_length = 50
                    rf_title_start = int(count_max/2- 25)
                else :
                    rf_title_length = count_max
                    rf_title_start = 0

                # print(combined)
                print(count_max)
                Label(master, text = "Feedback Resistor (Rf) Values: ", padx = 5, pady = 5, relief = "groove").grid(row= 0, column= rf_title_start, columnspan = rf_title_length, sticky = N+E+S+W)
                Label(master, text = "Branch: ", padx = 5, pady = 5, relief = "groove").grid(row = 0, column = 0, rowspan = 2, sticky = N+E+S+W)
                Frame(master, bd = 0, bg = "black", height = 2).grid(row = 2, column = 0, columnspan = count_max + 2, sticky = N+E+S+W)
                Frame(master, bd = 0, bg = "black", width = 2).grid(row = 0, column = 1, rowspan = len(combined)+ 3, sticky = N+E+S+W)
                count = 0
                for i in range(3) :
                    for j in range(len(rf[i])) :
                        print((i,j))
                        string = ""
                        for k in range(len(rf[i][j])) :
                            if (type(rf[i][j][k]) != type([1])) :
                                string += str(rf[i][j][k])
                            else : 
                                for l in range(len(rf[i][j][k])) :
                                    string += str(rf[i][j][k][l])
                                    if (l != len(rf[i][j][k]) - 1) :
                                        string += " || "

                            if (k != len(rf[i][j]) - 1) :
                                string += " + "
                        Label(master, text = string, padx = 5, pady = 5, relief = "groove").grid(row = 1, column = 2 + count, columnspan = rf_columns[i][j], sticky = N+E+S+W)

                        # if (i == 0) :
                        #     Label(master, text = rf[i][j], padx = 5, pady = 5, relief = "groove").grid(row = 1, column = 2 + count, columnspan = rf_columns[i][j], sticky = N+E+S+W)
                        # elif (i == 1) :
                        #     Label(master, text = str(rf[i][j][0]) + "+" + str(rf[i][j][1]), padx = 5, pady = 5, relief = "groove").grid(row = 1, column = 2 + count, columnspan = rf_columns[i][j], sticky = N+E+S+W)
                        # else : 
                        #     Label(master, text = str(rf[i][j][0]) + "||" + str(rf[i][j][1]), padx = 5, pady = 5, relief = "groove").grid(row = 1, column = 2 + count, columnspan = rf_columns[i][j], sticky = N+E+S+W)
                        
                        for k in range(len(combined)) :
                            # Label(master, text = k, padx = 5, pady = 5, relief = "sunken").grid(row = 2 + k, column = 0, sticky = N+E+S+W)
                            Label(master, text = str(k) + "  (" + str(ratio[k])+ ")", padx = 5, pady = 5, relief = "groove").grid(row = 3 + k, column = 0, sticky = N+E+S+W)
                            inter_count = 0
                            for item in combined[k][i] :
                                if (item[1] == rf[i][j]) :
                                    # Label(master, text = item[0], padx = 5, pady = 5, relief = "groove").grid(row = 2 + k, column = 1 + count + inter_count, sticky = N+E+S+W)
                                    # Label(master, text = item[0], padx = 5, pady = 5, relief = "groove").grid(row = 3 + k, column = 2 + count + inter_count, sticky = N+E+S+W)
                                    # print(1 + count + inter_count) 
                                    if (i == 0) :
                                        Label(master, text = item[0], padx = 5, pady = 5, relief = "groove").grid(row = 3+k, column = 2 + count + inter_count, columnspan = 1, sticky = N+E+S+W)
                                    elif (i == 1) :
                                        Label(master, text = str(item[0][0]) + "+" + str(item[0][1]), padx = 5, pady = 5, relief = "groove").grid(row = 3+k, column = 2 + count + inter_count, columnspan = 1, sticky = N+E+S+W)
                                    else : 
                                        Label(master, text = str(item[0][0]) + "||" + str(item[0][1]), padx = 5, pady = 5, relief = "groove").grid(row = 3+k, column = 2 + count + inter_count, columnspan = 1, sticky = N+E+S+W)
                                    inter_count += 1
                        count += rf_columns[i][j]



                    # print("Single: ")
                    # print(combined[a][0])
                    # print("Series: ")
                    # print(combined[a][1])
                    # print("Parallel")
                    # print(combined[a][2])


                    # print(temp_branch_vals)
                    # branch_vals[a] = temp_branch_vals

    # print(combined)
    mainloop()
    return combined



