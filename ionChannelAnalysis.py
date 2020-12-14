import sys
import neuron
import numpy as np
neuron.h.load_file('stdrun.hoc')
import matplotlib.pyplot as plt


'''
Ion channel analysis 

To get more functions for NEURON - https://neuron.yale.edu/neuron/static/docs/neuronpython/firststeps.html

if you want to load a morphology:

neuron.h.load_file('import3d.hoc')
imorphology = neuron.h.Import3d_SWC_read()
imorphology.input("morphology/MTC180800A-IDB-cor-rep.swc")
morphology_importer = sim.neuron.h.Import3d_GUI(imorphology, 0)
morphology_importer.instantiate(icell)

But then you have to iterate through the whole morphology to add all the ion channels using  for sec in simulator.neuron.h.allsec()
    
'''

channel = "naf"  #Name of the channel you want to analyse

soma=neuron.h.Section(name='soma') # Create a soma to start with, you can also create a dendrite and then connect them via "dend.connect(soma(1))"
soma.insert(channel) # Insert channel into soma, by repeating this command for different channels you can add as many as you like
setattr(soma,"gbar_"+channel,1) #Set conductance to 1 nS - for units used in neuron - https://www.neuron.yale.edu/neuron/static/docs/units/unitchart.html
neuron.h.celsius=35 #In most experiments we use 35 celsius, 

#soma.ek=-100 #Using Nernest equation, we found that the reversal potential in our experiments is around -100 mV for potassium, if your channel is potassium uncomment this line
soma.ena=50 # Same as above but for sodium, if you have both potassium and sodium channels, both these lines should be uncommented. 
	    # You can change the reversal if you want to see the effect on driving force

neuron.h.psection() #Check the structure of your cell 

current= list()
voltage =np.arange(-110,50,10) # Set the interval in which you would like to do the voltage clamp

for vinit in voltage:

    '''
     Point processes are different from ion channels (which are distributed) - https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/mechanisms/mech.html
     You can add point processes to any segment, use 0.5 (i.e. in the middle of the section for now 
    '''
    
    stim=neuron.h.SEClamp(soma(0.5)) # Here we put a voltage clamp in the middle of the soma
    stim.rs=1e-6 # One of the parameters you can set for voltage clamp. Try putting import pdb; pdb.set_trace() and run dir(stim) to see the parameters associated with stim
    stim.dur1 = 200
    stim.amp1=vinit
    
    neuron.h.tstop=200 
    neuron.h.v_init=vinit
    neuron.h.init()

    # You can extract all parameters which are defined as RANGE in the modfile, eg mechanisms/naf_ms.mod for this ion channel,
    # parameter is accessed via "parameteryouwant_ionchannelmodelname", here ina_naf_ms
    
    ionChannelCurrent=getattr(soma,"ina_"+channel)  # get the current from sodium channel, ik for potassium

    current.append(ionChannelCurrent)

    neuron.h.run()

    print(soma.v) # You can compare the voltage you set with the voltage clamp and the one you observe in the soma, change the stim.rs (resistance) and you will see an effect


print(max(map(abs,current))) # Absolute value of current, you can choose to plot it in another way

plt.plot(voltage,current, label=channel)
plt.title(channel)
plt.xlabel("Membrane potential (mV)")
plt.ylabel("Current (nA)")
plt.legend()
plt.savefig("IonChannelOutput/Output-Test.png")
plt.show()

'''
Current clamp 
stimobj = new IClamp(x)

del -- ms

dur -- ms

amp -- nA

i -- nA


An example of a  synapse

syn = new Exp2Syn(x)

syn.tau1 --- ms rise time

syn.tau2 --- ms decay time

syn.e -- mV reversal potential

syn.i -- nA synaptic current
'''



