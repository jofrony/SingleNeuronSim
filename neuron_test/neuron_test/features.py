import elephant as elp
import neo
import quantities as pq
import numpy as np


def number_of_action_potentials(voltage,parameters):

    neo_voltage = neo.AnalogSignal(np.array(voltage) * pq.mV, sampling_period=parameters["dt"] * pq.ms, units='mV')
    spike_train = elp.spike_train_generation.peak_detection(neo_voltage, threshold=-20 * pq.mV)

    num_ap = len(spike_train)

    return num_ap

    return num_spikes
