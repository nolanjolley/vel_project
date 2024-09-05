#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:37:22 2022

@author: nolanjolley

view the demo PLEASE: 
https://drive.google.com/file/d/1aO3XGVloeSkYE9qz4G8ztH5Ztpsj8HgO/view
"""

import csv

file_menu = "Please picke a file to analyze. Your options are:\n\
    1. cardboard\n\
    2. juggle\n\
    3. reg_bounce\n\
    Select a file (1-3): \n"
    
error_msg1 = "Error in file option."


def open_file(): 
    x = True
    while x == True: 
        option = input(file_menu)
        try: 
            option = int(option)
            
            if option == 1: 
                file_pointer = open("carboard.csv", "r")
                x = False
            elif option == 2: 
                file_pointer = open("juggle.csv", "r")
                x = False
            elif option == 3: 
                file_pointer = open("reg_bounce.csv", "r")
                x = False
            else: 
                print(error_msg1)
        
        except ValueError: 
            print(error_msg1)
    return(file_pointer)



def get_data(fp): 
    reader = csv.reader(fp)
    file_data = []
    next(reader)
    next(reader)
    
    
    for line in reader: 
        time = line[0]
        time = float(time)
        
        posy = line[1]
        posy = float(posy)
        
        vely = line[2]
        if vely == "": 
            vely = 0
        vely = float(vely)
        
        accy = line[3]
        if accy == "": 
            accy = 0 
        accy = float(accy)
        
        data = (time,posy,vely,accy)
        file_data.append(data)
        
    return(file_data)   

def get_changes(file_data):
    
    pos_time_changes = []
    
    for count, tup in enumerate(file_data): 
        
        vel = tup[2]
        time = tup[0]
        accy = tup[3]
        
        if count == 0: 
            dx = tup[1]
            dt = 0 
            dydt1 = dt, dx, time, accy
            pos_time_changes.append(dydt1)
            continue
        if count == 1: 
           pos = file_data[count][1]
           prevpos = file_data[count-1][1]
           
           time = file_data[count][0]
           prevtime = file_data[count-1][0]
           
           delx = pos - prevpos
           delt = time - prevtime
           dydt = (delt, delx, time, accy, vel)
           pos_time_changes.append(dydt) 
           
        else: 
            pos = file_data[count][1]
            prevpos = file_data[count-1][1]
            
            time = file_data[count][0]
            prevtime = file_data[count-1][0]
            
            delx = pos - prevpos
            delt = time - prevtime
            dydt = (delt, delx, time, accy)
            pos_time_changes.append(dydt)
    return(pos_time_changes)

def get_velocities_acc(pos_time):
    vel_list = []
    for x in range(len(pos_time)): 
        vel_list.append([])
    for count, tup in enumerate(pos_time): 
        dt = tup[0] 
        time = tup[2]
        acc = tup[3]
        if count == 0:
            vel = 0.0
            tup = (time,vel)
            vel_list[count]+=(time,vel)
        elif count == 1: 
            vel = tup[4]
            tup = (time,vel)
            vel_list[count]+=(tup)
            
        else:
            
            vel = (vel_list[count-1][1]) + (acc*dt)
            tup = (time,vel)
            vel_list[count] += (tup)
    
    return(vel_list)

def get_velocities_avg(data): 
    vel_list = [[]]
    for x in range(0,len(data)-1):
        vel_list.append([])
    for count, tup in enumerate(data): 
        time = tup[0]
        pos = tup[1]
        if pos != 0: 
            vel = time/pos
        else: 
            vel = 0 
        if pos > data[count-1][1]: 
            vel = abs(vel)
        vel_list[count].append(time)
        vel_list[count].append(vel)
    
    return(vel_list)  

def error(data, vel_time): 
    vely_list = []
    my_vely_list = []
    error_list = []
    
    for line in data: 
          vely = line[2]
          if vely == "": 
              vely = 0
          vely = float(vely)
          vely_list.append(vely)
          
    for l in vel_time: 
        my_vel = l[1]
        my_vely_list.append(my_vel)
    
    for x in range(len(vel_time)):
        if vely_list[x] == 0: 
            continue
        error = (my_vely_list[x] - vely_list[x]) / vely_list[x]
        error_list.append(error)
    total_error = sum(error_list)
    avg_error = total_error / len(error_list)
    avg_error = abs(avg_error*100)
    

    return(avg_error)
    
#sources of error:
    #all calculations assume one-dimensional y-orientated motion and tracker does not
    #in the case of juggling, the ball moves forward and backward closer and farther from the camera so error is greatly increased
    


#def display_ball(data): 
  
def main(): 

    x = True
    while x == True:
        fp = open_file()
        print("Generating data... \n")
        data = get_data(fp)
        print("Data generated.\n")
        
        print("How would you like to proceed?")
        option = input("\n1. Calcululate Velocities using kinematic equation 1 \n\
                       \n2. Calculate Velocities using change in position and change in time \n")
                       
        if option in "12": 
            
            if option == "1": 
                print("Analyzing data...\n")
                changes = get_changes(data)
                print("Getting velocities...\n")
                vel_time = get_velocities_acc(changes)
                error2 = error(data, vel_time)
                print("Velocities calculated with %{:.2f} error\n".format(error2))
                
                y = True
                while y == True:
                    optionB = input("Would you like to see the velocities? (Y/N) \n")
                
                    if optionB.lower() in "ny": 
                        y = False
                        if optionB.lower() == "y": 
                            print("{:<10s}{:<10s}".format("Time", "Velocity"))
                            for tup in vel_time: 
                                time = tup[0]
                                vel = tup[1]
                                print("{:<10.2f}{:<10.2f}".format(time,vel))
                        if optionB.lower == "n":
                            continue
                    else: 
                        print("Error with option\n")
                        
                z = True
                while z == True:
                    cont = input("Would you like to test another file? (Y/N) \n")
                
                    if cont.lower() in "yn":
                        z = False
                        if cont.lower() == "y": 
                            continue
                        
                        else: 
                            print("Thank you.\n")
                            x = False
                    else: 
                        print("Error with option\n")
                            
            if option == "2":
                
                print("Analyzing data...\n")
                changes = get_changes(data)
                print("Getting velocities...\n")
                vel_avg = get_velocities_avg(changes)
                error1 = error(data, vel_avg)
                print("Velocities calculated with %{:.2f} error\n".format(error1))
                
                k = True
                while k == True:
                    optionB = input("Would you like to see the velocities? (Y/N) \n")
                
                    if optionB.lower() in "ny": 
                        k = False
                        if optionB.lower() == "y": 
                            print("{:<10s}{:<10s}".format("Time", "Velocity"))
                            for tup in vel_avg: 
                                time = tup[0]
                                vel = tup[1]
                                print("{:<10.2f}{:<10.2f}".format(time,vel))
                        if optionB.lower == "n":
                            continue
                    else: 
                        print("Error with option\n")
                        
                    w = True
                    while w == True:
                        cont = input("Would you like to test another file? (Y/N) \n")
                    
                        if cont.lower() in "yn":
                            w = False
                            if cont.lower() == "y": 
                                continue
                            
                            else: 
                                print("Thank you.\n")
                                x = False
                        else: 
                            print("Error with option\n")
            
        else: 
            print("Error in option\n")


    
if __name__ == "__main__":
    main()
