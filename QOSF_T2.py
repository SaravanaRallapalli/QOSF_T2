# -*- coding: utf-8 -*-


import numpy as np
from qiskit import QuantumCircuit
#from qiskit.quantum_info import Statevector 
from qiskit.visualization import plot_histogram
from qiskit import Aer,execute
import random
import qiskit.providers.aer.noise as noise
circuit = QuantumCircuit(2,2)


prob_1 = 0.05  # 1-qubit gate
prob_2 = 0.05   # 2-qubit gate

error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

noise_model=noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ['ry'])   #Error for RY gate
noise_model.add_all_qubit_quantum_error(error_2, ['cx'])   #Error for CX gate


bac_sim=Aer.get_backend('qasm_simulator')
dv=[1,0,0,0]
def grad_desc(mycircuit,s):
    x=random.random()                         #random x,y
    y=random.random()
    
    n=300
    for i in range(n): 

       xd_n=0.5*(np.sin(2*x))*(pow(np.sin(y/2),4))                      #from cost function given in PDF
       yd_n=0.5*(np.sin(y))*(1+(pow(np.sin(y),2))*(1+pow(np.cos(x),2)))
       x=x+0.2*xd_n
       y=y+0.2*yd_n
       
       if i==n-1:
           mycircuit.ry(x,0)
           mycircuit.cx(0,1)
           mycircuit.ry(y,0)   
           #mycircuit.draw('mpl')
           mycircuit.measure([0,1],[0,1])
           p=execute(mycircuit,bac_sim,noise_model=noise_model,shots=s)
           res=p.result()
           counts=res.get_counts(mycircuit)
           plot_histogram(p.result().get_counts(), title="Measurement for shots = 1000")
           #print(x,y,counts)
           return x,y
c=grad_desc(circuit,1000)
#print(c)

#     BONUS TASK

x=c[0];y=c[1]
circuit.initialize(dv,[0,1])
circuit.ry(x,0)
circuit.cx(0,1)
circuit.ry(y,0)
circuit.ry(np.pi/2,0)
circuit.ry(np.pi/2,1)
circuit.measure([0,1],[0,1])
p=execute(circuit,bac_sim,noise_model=noise_model,shots=1000)
res=p.result()
counts=res.get_counts(circuit)

if (counts['01']+counts['10'])/2>=400:
    x=-x

if (counts['11']+counts['11'])/2>=400:
    x=x
circuit.initialize(dv,[0,1])
circuit.ry(x,0)
circuit.cx(0,1)
circuit.ry(y,0)

backend = Aer.get_backend('statevector_simulator')
job = execute(circuit, backend)
result = job.result()            
outputstate = result.get_statevector(circuit, decimals=3)
print("parameters for required output state are:")
print("x=",x,"y=",y)                                         #parameters for gates shown in figure! in PDF
print(outputstate)                                           #(|01>+|10>)/sqrt(2)