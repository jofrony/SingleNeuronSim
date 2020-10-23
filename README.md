# NEURON-practice
Testing multicompartmental models and ion channel analysis

One can either do a git clone https://github.com/jofrony/NEURON-practice.git or download the zip on the right hand side under the clone or download - button

To run the code you need some extra python modules:

```python
pip install packagename

```

numpy
json
bluepyopt
neurom
matplotlib
neuron

Install NEURON and python: https://neuron.yale.edu/neuron/getstd

## Steps!

When you have downloaded the folder and installed NEURON and python modules, you have to start by running "nrnivmodl mechanisms/" in the folder.
Then you can either run:
```python
python ionChannelAnalysis.py 

```
for running simulations on individual ion channel models. And run:

```python
python manualTuningModel.py

```

for running the whole model. In "modelParameter.txt", one can change the parameters which are then loaded into the model.

If you want to analyse the morphology you can use morphologyAnalysis.py, which also contains additional links to NeuroM software. 

[![DOI](https://zenodo.org/badge/270691300.svg)](https://zenodo.org/badge/latestdoi/270691300)

