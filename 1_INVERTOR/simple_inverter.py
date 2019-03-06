####################################################################################################
#-#-#-#-#-#-#-#-#   ============================================================   #-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#                       Ex 1: Simple Inverter                      #-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#   ============================================================   #-#-#-#-#-#-#-#-#
####################################################################################################

import os
from help_functions import *

import matplotlib.pyplot as plt

import re
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Netlist import SubCircuitFactory
from PySpice.Unit import *


####################################################################################################
# IMPORT SPICE NETLIST OF CIRCUIT:

spice_library = SpiceLibrary('../libraries/')
netlist_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'simple_inverter.sp')
parser = SpiceParser(path=netlist_path)
circuit = parser.build_circuit()
circuit.include(spice_library['INVERTER'])


####################################################################################################
# CONFIGURE VOLTAGE SOURCES

supply = 1@u_V
circuit.PulseVoltageSource('Vin', 'input', 'vss',
                                initial_value=circuit.gnd,
                                pulsed_value=supply,
                                delay_time=0.99@u_ps,
                                rise_time=20@u_ps,
                                fall_time=20@u_ps,
                                pulse_width=1@u_ns,
                                period=2@u_ns)
circuit.V('supply', 'vdd', 'vss', supply)
circuit.V('ground', 'vss', circuit.gnd, circuit.gnd)


####################################################################################################
# SIMULATE IMPORTED CIRCUIT

print("Simulated circuit:")
print(str(circuit))

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=0.001@u_ns, end_time=5@u_ns)


####################################################################################################
# CALCULATE DELAY

figure = plt.figure(1, (20, 10))
print('Power Supply: {0:.2f} V'.format(supply.value))
(incros_x, incros_y) = findFirstCrossingWithValue(analysis['input'], supply.value/2)
(outcros_x, outcros_y) = findFirstCrossingWithValue(analysis['output'], supply.value/2)

delay = (outcros_x-incros_x)*1e12
print('Delay tp0: {0:.3f} ns'.format(delay))


####################################################################################################
# PLOT RESULTS OF SIMULATION

figure = plt.figure(1, (20, 10))
plot(analysis['input'])
plot(analysis['output'])
#plt.plot([incros_x, outcros_x], [incros_y, outcros_y], 'ro')
plt.legend(('Vin [V]', 'Vout [V]'), loc=(.8,.8))
plt.grid()
plt.xlabel('t [s]')
plt.ylabel('Vin [V]')

plt.tight_layout()
plt.show()
