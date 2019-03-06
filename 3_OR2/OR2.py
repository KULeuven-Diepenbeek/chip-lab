####################################################################################################
#-#-#-#-#-#-#-#-#   ============================================================   #-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#                       Ex 3: OR2                                  #-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#   ============================================================   #-#-#-#-#-#-#-#-#
####################################################################################################

import os
# from help_functions import *

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
netlist_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'OR2.sp')
parser = SpiceParser(path=netlist_path)
circuit = parser.build_circuit()

circuit.include(spice_library['INVERTER'])
circuit.include(spice_library['OR2'])


####################################################################################################
# CONFIGURE VOLTAGE SOURCES

supply = 1@u_V
circuit.V('supply', 'vdd', 'vss', supply)
circuit.V('ground', 'vss', circuit.gnd, circuit.gnd)


####################################################################################################
# SIMULATE IMPORTED CIRCUIT

print("Simulated circuit:")
print(str(circuit))

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=0.001@u_ns, end_time=4@u_ns)


####################################################################################################
# PLOT RESULTS OF SIMULATION

plt.subplot(2, 1, 1)
plot(analysis['A'])
plot(analysis['B'])
plt.title('OR2')
plt.legend(('A [V]', 'B [V]'), loc=(.8,.8))
plt.ylabel('Vin [V]')

plt.subplot(2, 1, 2)
plot(analysis['output'])
plt.xlabel('t [s]')
plt.ylabel('Vout [V]')
plt.tight_layout()
plt.show()
