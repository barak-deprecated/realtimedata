'''
Collect and Plot
Last updated 9/16/14

This script collects serial data and plots it after user command.

Expected Serial Data Format:

time    x1      x2      ...     xn
 |      |       |       ...     |
 v      v       v       ...     v
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t  ...\t   x.x \n
'''

import sys, select, serial, time
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# constants
PORT_NAME = '/dev/tty.usbmodem411'
BAUDRATE = 115200

# create a deque storage container for quick data storage
data_storage = deque()

# wait for the user to hit enter before beginning data collection
start = input("Press <enter> to start collecting data")
print("Opening and resetting serial port...")

# open serial port
ser = serial.Serial(port=PORT_NAME, baudrate=BAUDRATE, timeout=1)

# Flush out the serial input buffer and prepare it to start reading clean data
ser.setDTR(False)  # Toggle DTR to reset microcontroller
time.sleep(1)
ser.flushInput() # toss any data already received
ser.setDTR(True)

print("Beginning data collection... press <enter> to stop...")

# loop will run until user hits enter
while True:
    data_storage.append(ser.readline())  # add the data to the right side of deque
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break

# close serial port
ser.close()

print("Data collection finished, serial port closed.")
print("Processing data...")

# pull the data out of the deque storage container and split the lines of characters
# also, filter out empty lines (which can come when first reading the input buffer)
data_matrix = [line.split() for line in data_storage if line]
# convert the list of lists of byte literals into a list of lists of floats
data_matrix = [[float(column) for column in row] for row in data_matrix]

# determine the number of data columns and the corresponding number of lines to plot
# (column 0 is reserved for time)
num_of_columns = len(data_matrix[0])
num_of_lines = num_of_columns - 1

# store the columns to be used as the x and y data for the lines
columns = []
for j in range(num_of_columns):
    column = [row[j] for row in data_matrix]
    columns.append(column)

# plot all the lines, taking user input for what to title them
lines=[]
labels=[]
for i in range(num_of_lines):   
    line, = plt.plot(columns[0], columns[i+1])
    lines.append(line)
    label = input("Enter label for data in column " + str(i+1) + " (0 index): ")
    labels.append(label)

print("Plotting...")
# plot the legend    
plt.legend(lines,
           labels,
           loc='upper center',
           prop={'size':10},
           bbox_to_anchor=(0.5, 1.07),
           ncol=3,
           )

# show the plot        
plt.show()

print("Thanks.")
# print("")
# print("What next?")
# print("[1] narrow line selection")
# print("[2] repeat data collection")
# print("[3] quit - I'm finished")
# choice = input("Enter yo' numba of selct'n here: ")
# if choice == "1":
#     while True:
#         lines_to_plot = input("Enter line #s you want to plot: ")
#         lines_to_plot = lines_to_plot.split()
#         
#         
# else if choice == "2":
#     pass
# 
# else:
#     sys.exit("Goodbye!") 
    
    
    