'''
Real Time Data
Last updated 9/16/14

This script plots real time serial data on a left-scrolling chart.

Expected Serial Data Format:

time    x1      x2      ...     xn
 |      |       |       ...     |
 v      v       v       ...     v
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t  ...\t   x.x \n
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial

# constants
PORT_NAME = '/dev/tty.usbmodem411'
BAUDRATE = 9600
NUM_OF_LINES = 1  # script expects 1 + num_of_lines data columns (1 for time)
XAXIS_RANGE = 10.0

# function that will drive the animation of FuncAnimation
# FuncAnimation mistakenly passes in an argument to animate, hence *args to absorb it
def animate(*args):
    # read line from serial port
    datarow = ser.readline().split()
    
    # data is read in as a list of binary literals. This cleans the data up into floats.
    if datarow:
        datarow = [float(value) for value in datarow]
    # after input buffer is flushed, the first reading might be empty. Just set it to 0.
    else:
        datarow = [0 for i in range(NUM_OF_LINES + 1)]
    
    # the independent variable (in this case t for time) is set to the value in the
    # first column
    t = datarow[0]
    
    # set the new x-axis limits. This gives the effect of a real time scrolling axis
    plt.xlim(t-XAXIS_RANGE, t)
    
    # expand the y-axis limits to meet peaks of incoming values
    #! Can this be replaced with some sort of autoscale?
    ymin, ymax = plt.ylim()
    if min(datarow[1:]) < ymin:
        plt.ylim(min(datarow[1:]), ymax)
    if max(datarow[1:]) > ymax:
        plt.ylim(ymin, max(datarow[1:]))
    
    # update the lines
    for i, line in enumerate(lines):
        line.set_xdata(np.append(line.get_xdata(), datarow[0]))
        line.set_ydata(np.append(line.get_ydata(), datarow[i+1]))


# set up figure and axes for plotting animation
fig, ax = plt.subplots()

# setup the lines to be updated and store the line objects and labels(as defined by user)
lines = []
labels = []
for i in range(NUM_OF_LINES):
    line, = ax.plot([], [])
    lines.append(line)
    label = input("Enter label for data in column " + str(i+2) + ": ")
    labels.append(label)

# create a legend for the plot
plt.legend(lines,
           labels,
           loc='upper center',
           prop={'size':10},
           bbox_to_anchor=(0.5, 1.07),
           ncol=3,
           )

# open serial port
ser = serial.Serial(port=PORT_NAME, baudrate=BAUDRATE, timeout=1)

# Flush out the serial input buffer and prepare it to start reading clean data
ser.setDTR(False)  # Toggle DTR to reset microcontroller
time.sleep(1)
ser.flushInput() # toss any data already received
ser.setDTR(True)

# create the matplotlib FuncAcnimation class that will manage updating the plot    
ani = animation.FuncAnimation(fig, animate, interval=1, blit=False)

# show the plot
plt.show()   