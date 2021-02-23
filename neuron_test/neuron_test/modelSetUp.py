def packageModel(handTuneFile):
    
    import numpy as np
    import json
    
    parameter_file = list()
    mechanism_file = dict()
    paraML = list()
    channel_list = list()  

    
    # infile=open(handTuneFile,'r') 
    modelHandTune = np.genfromtxt(handTuneFile, dtype=None)
    
    for dataLine in modelHandTune:

        
        
        channelInfo = str(dataLine[0].decode("utf-8")).split(".")

        if channelInfo[0] in ["v_init", "celsius"]:
            paraML.append({"param_name":channelInfo[0] , "type": "global", "value": dataLine[1]})

        elif channelInfo[0] in ["g_pas","e_pas","cm","Ra","ek","ena"]:
            paraML.append({"dist_type": "uniform", "param_name": channelInfo[0],"sectionlist": channelInfo[1],\
                           "type": "section", "value": dataLine[1]})
            

        else:
             paraML.append({"param_name": channelInfo[0], "type": "range", \
                            "sectionlist": channelInfo[1], "dist_type": "uniform", \
                            "value": dataLine[1]})


    mechanism_file.update({"soma" : ["pas","cadyn_fs"]})
    mechanism_file.update({"basal" : ["pas"]})
    mechanism_file.update({"axonal" : ["pas"]})
    
    for index in range(len(paraML)):
        
        potentialChannel=paraML[index]["param_name"].split("_")
        
        parameter_file.append(paraML[index])

        
        if len(potentialChannel)>2:

            
            
            ionChannelName = "_".join(potentialChannel[1:])

            if ionChannelName not in mechanism_file[paraML[index]["sectionlist"]]:
                mechanism_file[paraML[index]["sectionlist"]].append(ionChannelName)
                                      
    
    parameters="config/parameters.json"
    mechanism="config/mechanisms.json"

    with open(mechanism,"w") as mechs:
        json.dump(mechanism_file,mechs)

    with open(parameters,"w") as param:
        json.dump(parameter_file,param)




