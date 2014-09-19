'''
Real Time Data

This script plots real time serial data on a left-scrolling chart.

Expected Serial Data Format:

time    x1      x2      ...     xn
 |      |       |       ...     |
 v      v       v       ...     v
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t 	...\t   x.x \n
x.x \t  x.x \t  x.x \t  ...\t   x.x \n

Last updated: 9/17/14
Author: Barak Alon
'''

import serial, time, sys, select
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

PORT_NAME = '/dev/tty.usbmodem411'    # serial port name depends on system
BAUDRATE = 9600

# Buffer size is in terms of number of "serial data rows to collect before  
# redrawing the plot." If the program is having trouble keeping up with
# incoming serial data, increase the buffer size.
BUFFER_SIZE = 5  

# The redraw interval tells the matplotlib Function based Animation to redraw
# the plot every ____ milliseconds.
REDRAW_INTERVAL = 50

# This is the number of data streams to plot (should be one less than columns).
NUM_OF_LINES = 3  

# X-Axis Range is the size of the x-limits to keep on screen as the chart 
# scrolls. If data is in seconds, this is how long a data point is on screen.
XAXIS_RANGE = 10.0  


def initialize_plot(number_of_lines):
	"""
	Set up the matplotlib figure to be plotted, collect the data labels
	from user, and return the line handles.
	"""
	line_objects = [] 
	labels = []
	
	# Create the line objects that will be plotted in real time.
	for i in range(number_of_lines):
		line, = plt.plot([], [])
		line_objects.append(line)
		label = input("Enter label for data in column " + str(i+2) + ": ")
		labels.append(label)
	
	# Create the plot legend, attaching the labels to their corresponding lines.
	plt.legend(line_objects,
			   labels,
			   loc='upper center',
			   prop={'size':10},
			   bbox_to_anchor=(0.5, 1.07),
			   ncol=3,
			   )
	
	return line_objects
           
def refresh_serial_port(serial_port):
    """
    Flush out the serial input buffer and reset the controller. 
    (Data can be all screwy when you first open a port. This helps clean it up.)
    """
    serial_port.setDTR(False)
    time.sleep(1)
    serial_port.flushInput()
    serial_port.setDTR(True)

def process_buffer(buf, number_of_lines):
    """
    Take the data in the buffer return neat data columns that we can use.
    (Data in the buffer is stored as lines of byte literals, and we want 
    columns of floats.)
    """
    # Split the byte literal lines into lists of byte literals.
    data = [line.split() for line in buf if line]
    
    # Convert each byte literal into a float.
    data = [[float(value) for value in row] for row in data]    
    
    # Transpose the data matrix (it works better with update_plot like this).
    cols = []
    for j in range(number_of_lines + 1):
        col = [row[j] for row in data]
        cols.append(col)
    
    return cols
    
def update_plot(line_objects, cols, x_range):
    """
    Take the line objects, add in the data from the buffer, and reset the plot.
    """
    # Update the x-values for every line as the time data, which should be
    # stored in column 0. Set the y-values from the rest of the columns.
    for i, line in enumerate(line_objects):
        line.set_data(np.append(line.get_xdata(), cols[0]), 
                      np.append(line.get_ydata(), cols[i+1]))                          
    
    # In order to scroll the plot to the left, the right x-limit should be the 
    # last time value from the buffer. The left x-limit should be that minus
    # the range of x-values to keep on the screen.
    last_time_value = cols[0][len(cols[0])-1]
    plt.xlim(last_time_value - x_range, last_time_value)
    
    # Relimit the y-axis and rescale the plot.
    ax = plt.gca()       # "gca" stands for "get current axes"
    ax.relim()
    ax.autoscale_view()
    
def animate(buffer, ser, lines, *args):
    """
    This is the function that drives the animation of the plotting.
    """
    global BUFFER_SIZE, NUM_OF_LINES, XAXIS_RANGE
    
    # Read a line from the serial input buffer and add it to our own buffer
    buffer.append(ser.readline())    

    # Flush the buffer if it reaches it's maximum size
    if len(buffer) >= BUFFER_SIZE:
		columns = process_buffer(buffer, NUM_OF_LINES)
		update_plot(lines, columns, XAXIS_RANGE)
		buffer[:] = []


def main():
	buffer = []

	print("Initializing plot and lines...")
	lines = initialize_plot(NUM_OF_LINES)

	print("Opening serial port " + 
		  PORT_NAME + " at " + str(BAUDRATE) + " baudrate...")           
	ser = serial.Serial(port=PORT_NAME, baudrate=BAUDRATE, timeout=1)

	print("Beginning data collection...")
	print("Press <enter> to stop...")
	refresh_serial_port(ser)
    
	fig = plt.gcf()     # "gcf" stands for "get current figure"
	
	# Animate the plot by repeatedly calling animate, passing it fargs
	ani = FuncAnimation(fig, 
	                    animate, 
	                    fargs=[buffer, ser, lines], 
	                    interval=REDRAW_INTERVAL,
	                    )
    
    plt.show()
    
    # Close the serial port, preventing the port from being frozen.
	print("Closing serial port...")        
	ser.close()


# Call the main function
if __name__ == '__main__':
  main()