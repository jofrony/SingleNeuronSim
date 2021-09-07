import json
import numpy as np

class DefineTestmodel:

    def __init__(self, name):
        self.name = name
        self.param_definition = list()
        self.param_definition_optimisation = list()
        self.mechanisms_definition = dict()
        self.mechanisms_loaded = None
        
    def load_mechanisms(self,mechanisms):

        with open(mechanisms,'r') as f:
            self.mechanisms_loaded = json.load(f)

        self.mechanisms_definition = self.mechanisms_loaded

    def load_parameters(self,parameters,id_num):

        with open(parameters,'r') as f:
            param_definition = json.load(f)[id_num]

        for p in param_definition:

            if 'morphology' not in p.keys():
                self.param_definition.append(p)
                
        
    def param(self,param,value,variable=None,type_param=None, section=None,variation=None):
        
        
        if type_param == 'global':
            self.param_definition.append({'param_name' : param,
                                          'type' : 'global',
                                          'value' : value})

            if variation is not None:

                self.param_definition_optimisation.append({'param_name' : param,
                                                           'type' : 'global',
                                                           'bounds' : sorted([np.round(value*variation[0],8),\
                                                                              np.round(value*variation[1],8)])})
            else:
                self.param_definition_optimisation.append({'param_name' : param,
                                          'type' : 'global',
                                          'value' : value})
                
                


        elif type_param == 'section':
            self.param_definition.append({'param_name' : param,
                                         'type' : 'section',
                                         'value' : value,
                                         'sectionlist' : section,
                                         'dist_type' : 'uniform'})

            if variation is not None:

                self.param_definition_optimisation.append({'param_name' : param,
                                                           'type' : 'section',
                                                           'bounds' : sorted([np.round(value*variation[0],8),\
                                                                       np.round(value*variation[1],8)]),
                                                           'sectionlist' : section,
                                                           'dist_type' : 'uniform'})
            else:
                self.param_definition_optimisation.append({'param_name' : param,
                                         'type' : 'section',
                                         'value' : value,
                                         'sectionlist' : section,
                                         'dist_type' : 'uniform'})
                
                

        elif type_param == 'range':
            self.param_definition.append({'param_name' :'_'.join([variable,param]),
                                         'type' : 'range',
                                         'value' : value,
                                         'sectionlist' : section,
                                         'dist_type' : 'uniform'})
            if variation is not None:

                self.param_definition_optimisation.append({'param_name' :'_'.join([variable,param]),
                                         'type' : 'range',
                                         'bounds' : sorted([np.round(value*variation[0],8),\
                                                     np.round(value*variation[1],8)]),
                                         'sectionlist' : section,
                                         'dist_type' : 'uniform'})
            else:
                self.param_definition_optimisation.append({'param_name' :'_'.join([variable,param]),
                                         'type' : 'range',
                                         'value' : value,
                                         'sectionlist' : section,
                                         'dist_type' : 'uniform'})
                

            self.mechanism_add(param,section)
            

    def dynamic_handling(self,param,section):

        self.mechanism_add(param,section)
        
    def mechanism_add(self,param,section):

        if section in self.mechanisms_definition.keys():

            if param not in self.mechanisms_definition[section]:
                self.mechanisms_definition[section].append(param)

        else:
            self.mechanisms_definition.update({section : list()})
            self.mechanisms_definition[section].append(param)


    def save_set_up(self,save_opt=False):

        parameters="config/parameters.json"
        parameters_opt="config/optimisation_parameters.json"
        mechanism="config/mechanisms.json"

        with open(mechanism,"w") as mechs:
            json.dump(self.mechanisms_definition,mechs)

        with open(parameters,"w") as param:
            json.dump(self.param_definition,param)
            

        if save_opt:
            with open(parameters_opt,"w") as param_opt:
                json.dump(self.param_definition_optimisation,param_opt)




        
        
        
