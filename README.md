realtimedata
============

Realtimedata is a python script using the matplotlib, pyserial, and numpy packages to process incoming data from a computer's serial port and plot it in real time.

It's important to edit the following global variables in the script when using it:

* PORT_NAME - The name of your serial port will depend on your system. 
* BAUDRATE - Make sure this is the same baudrate that your controller is sending data to the computer at.
* BUFFER_SIZE - This defines how many *lines to keep in the buffer* before flushing it to be processed and plotted. This significantly decreases the amount of times that matplotlib has to redraw the plot and should be increased if the script is having trouble keep up with incoming serial data.
* NUM_OF_LINES - This is simply the amount of lines to plot, or in other words the amount of data stream coming in. It should be one less than the number of columns (because the 0th column is reserved for time).
* XAXIS_RANGE - The plot is left scrolling with time - this essentially defines how long to keep data on the plot. If your time data is coming in seconds, this is the time it takes in seconds for data to get from the right side of the plot to the left.

It's still a work in progress, but by all means, have at it.
