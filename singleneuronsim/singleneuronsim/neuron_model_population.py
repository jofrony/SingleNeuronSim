from mpi4py import MPI
from neuron import h
from singleneuronsim.Neuron_model_extended import NeuronModel
import os
import logging
from singleneuronsim.NrnSimulatorParallel import NrnSimulatorParallel
import numpy as np
class NeuronModelPopulation:

    def __init__(self,mechanisms,parameters,morphology,variations):

        self.variations = int(variations)
        self.mechanisms = mechanisms
        self.parameters = parameters
        self.morphology = morphology
        self.neurons = dict()
        self.sim = NrnSimulatorParallel(cvode_active=False)
        self.v_save = dict()
        self.t_save = dict()
        self.i_stim = list()

    def set_gidlist(self, gidlist):

        self.gidlist = gidlist

    def set_gids(self):

        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        pc = h.ParallelContext()
        self.pc = pc
        self.gidlist = []

        for i in range(int(pc.id()), self.variations, int(pc.nhost())):
            self.gidlist.append(i)


    def start_logging(self):

        directory = "logfiles"

        if not os.path.exists(directory):
            os.makedirs(directory)

        logging.basicConfig(filename="logfiles/log-file-" + str(self.gidlist[0]) + ".log", level=logging.DEBUG)


    def setup_neurons(self):
        logging.info('This worker : ' + str(len(self.gidlist)))

        for k in range(len(self.gidlist)):

            self.neurons[k] = NeuronModel(cell_name='test', morph_file=self.morphology, mech_file=self.mechanisms,param_file=self.parameters, id_num=self.gidlist[k])


    def instantiate(self):

        for i, cell in self.neurons.items():
            self.neurons[i].instantiate(sim=self.sim)

    def time_save(self):

        self.t_save = self.sim.neuron.h.Vector()
        self.t_save.record(self.sim.neuron.h._ref_t)

        return self.t_save

    def voltage_save(self):

        for i, cell in self.neurons.items():
            v = self.sim.neuron.h.Vector()
            v.record(getattr(cell.icell.soma[0](0.5), '_ref_v'))
            self.v_save[i] = v

        return self.v_save

    def run(self,tstop):

        self.sim.neuron.h.tstop = tstop
        self.sim.neuron.h.run()


    def protocols(self,protocol):

        for i, cell in self.neurons.items():
            cur_stim = self.sim.neuron.h.IClamp(0.5, sec=self.neurons[i].icell.soma[0])
            cur_stim.delay = protocol['parameters']["start"]
            cur_stim.dur = protocol['parameters']["duration"]
            cur_stim.amp = protocol['parameters']["amp"]
            self.i_stim.append(cur_stim)


    def save_voltages(self, downsample=1):

        world_voltage = self.comm.gather(self.v_save, root=0)
        gidlist = self.comm.gather(self.gidlist,root=0)

        self.pc.barrier()

        if self.rank == 0:

            reorder = dict()
            voltage_saves = list()

            voltage_saves.append(np.array(list(self.t_save))[::downsample])

            for i,volt in enumerate(world_voltage):

                for k in range(len(gidlist[i])):
                    volt_recording = volt[k]
                    reorder.update({gidlist[i][k]:volt_recording})

            for keys in sorted(reorder):
                volt_recording = reorder[keys]
                volt_array = np.array(list(volt_recording))
                voltage_saves.append(volt_array[::downsample])

            np.savetxt("voltages.csv", voltage_saves)

    
