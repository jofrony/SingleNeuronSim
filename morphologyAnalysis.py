'''
#######################################################################

Morphology tool for visualising 
https://github.com/BlueBrain/NeuroM (Some code on visualisation is included further down)




#######################################################################

'''

import neurom as nm
from neurom import viewer
from neurom.view import plotly

morphologyFile = "morphology/MTC180800A-IDB-cor-rep.swc"


'''
 NeuroM https://github.com/BlueBrain/NeuroM

'''

nrn = nm.load_neuron(morphologyFile)

'''
Examples of features which you can extract from NeuroM - You can find more on:

https://github.com/BlueBrain/NeuroM/blob/fd64d2a45644119fa01e61fe8f6a701113deb78c/neurom/features/__init__.py

You can look into the swc-file in the morphology folder - the structure of the file is explained at, 
http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html

'''

total_area_per_neurite = nm.get('total_area_per_neurite', nrn, neurite_type=nm.BASAL_DENDRITE)
volume_basal_dendrite = nm.get('neurite_volumes', nrn, neurite_type=nm.BASAL_DENDRITE)
soma_surface_areas = nm.get('soma_surface_areas', nrn)
dendrite_length = nm.get('neurite_lengths', nrn, neurite_type=nm.BASAL_DENDRITE)

dend_area_total = sum(total_area_per_neurite)
dend_length_total = sum(dendrite_length)
soma_area = soma_surface_areas[0]

print("soma area : ",soma_area)
print("dend area : ",dend_area_total)
print("dendritic length : ",dend_length_total)

fig, ax = plotly.draw(nrn, plane='xy')
fig, ax = plotly.draw(nrn)


'''
If you want to do other forms of analysis check out, https://notebooks.gesis.org/binder/jupyter/user/bluebrain-neurom-xhl01s7f/notebooks/tutorial/getting_started.ipynb

'''
