# simstream
A utility for user-defined remote system and simulation data monitoring.

## Dependencies
Tested with Python 2.7.11 and 3.5.1
* tornado >= 4.3 (`pip install tornado`)

## Installation
1. Clone this repository
2. `python setup.py install`

## Running the Example
The example runs a simple collector that records the maximum memory used by the server (MB) and a timestamp. It also generates a plot of the results.
1. From the repository root, run `python example/memory_consumption.py`
2. Open a browser
3. Navigate to http://localhost:8888/viewmem/ to view the plot
