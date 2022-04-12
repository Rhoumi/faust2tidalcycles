import os
import sys
import os.path
from os import path
import json
from collections import ChainMap
import subprocess
import platform
import shutil

#####################################
######▄▄▄#▄▄▄▄▄▄▄#▄▄▄▄▄▄▄#▄▄####▄#### 
#####█   █       █       █  █##█ █###
#####█   █  ▄▄▄▄▄█   ▄   █   █▄█ █###
##▄##█   █ █▄▄▄▄▄█  █ █  █       █###
#█ █▄█   █▄▄▄▄▄  █  █▄█  █  ▄    █###
#█       █▄▄▄▄▄█ █       █ █ █   █###
#█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█  █▄▄█###
#####################################

# Opening JSON file
with open('gliitchi.dsp.json') as json_file:
    json_data = json.load(json_file)
 
    # Print the type of data variable
  #  print("Type:", type(json_data))
 
    # Print the data of dictionary
    
    my_inputs = json_data['inputs']
    my_outputs = json_data['outputs']
    my_name = json_data['name']

    

   # my_arguments = json_data['address']
    
 #WIP   
"""    if "address" in json_data :
        my_arguments = ''
        my_arguments = my_arguments.join(json_data['address'])
    elif 'address' in json_data['ui'] :
        my_arguments = my_arguments.join(json_data['address'])
    elif 'address' in json_data['items'] :
        my_arguments = my_arguments.join(json_data['address'])
        
    print(my_arguments)

    
 """
    
""" 
 / \------------------, 
 \_,|                 | 
    |    Coresynths   | 
    |  ,----------------
    \_/_______________/     
    
"""
def get_coresynths_filepath(filename:str ='core-synths.scd'):
    """ 
    Return the filepath of core-synths.scd. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

 

def cs_placeholder_filler(synth_name: str, nb_inputs : int, argument_list: list):
    """ Inserting arguments in placeholder SynthDef """
    template = '''\n    SynthDef(\"{synth_name}\" ++ ~dirt.numChannels, {{
        | {in_list},{argument_list}|
        var signal = In.ar(out, ~dirt.numChannels);
        signal = {synth_name}.ar({signal_beg},{signal_argument}, out);
        ReplaceOut.ar(out, signal);
         }}).add;
    \n
    '''
    ###add one "signal" by inputs
    signal_beg="signal"
    for x in range(1, nb_inputs, 1):
        signal_beg = signal_beg+",signal"
        
    ###add in%s by inputs
    in_list = "in0"
    for x in range(1, nb_inputs, 1):
        in_list = in_list+",in%s" % x
    
    
    argument_beautify = ', '.join(argument_list)
    return template.format(synth_name=synth_name, 
                           argument_list=argument_beautify,
                           signal_argument=argument_beautify,
                           nb_inputs=nb_inputs,
                           signal_beg=signal_beg,
                           in_list=in_list)

def cs_find_last_occurence(filepath: str, pattern: str):
    """ Find the last occurence of pattern in file and return line """
    last_occurence = 0

    with open(filepath, 'r') as file:
        for index, line in enumerate(file.readlines()):
            if pattern in line:
                last_occurence = index

    return last_occurence
        

def cs_inject_new_definition(text_content: str, filepath: str):
    """ Inject new definition in core-synths.scd """
    index = cs_find_last_occurence(filepath, pattern=".add;")

    # Looking for the last .add in file, adding right after it

    # Reading file into memory
    with open(filepath, "r") as f:
        contents = f.readlines()

    # injecting new definition
    contents.insert(index+1, text_content)

    # Writing definition to file
    with open(filepath, "w") as f:
        contents = "".join(contents)
        f.write(contents)

    return True
"""
 / \------------------, 
 \_,|                 | 
    |    Coremodules  | 
    |  ,----------------
    \_/_______________/ 
"""

def get_coremodules_filepath(filename:str ='core-modules.scd'):
    """ 
    Return the filepath of core-modules.scd. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

    


def cm_placeholder_filler(synth_name: str, argument_list: list):
    """ Inserting arguments in placeholder """
    template = '''\n      ~dirt.addModule('{synth_name}',
        {{|dirtEvent|
            dirtEvent.sendSynth('{synth_name}' ++ ~dirt.numChannels,
            [ 
                {parameters},
                out: ~out
            ])
            }});
    \n'''
    parameters = ["{x}: ~{x}".format(x=x) for x in argument_list]
    # weird formatting to match default file
    parameters = ",\n                ".join(parameters)
    parameters = parameters.replace('"', '')
    return template.format(synth_name=synth_name, 
            parameters=parameters)

def cm_find_penultimate_occurence(filepath: str, pattern: str):
    """ Find the penultimate occurence of pattern in file and return line """
    penultimate_occurence = 1

    with open(filepath, 'r') as file:
        for index, line in enumerate(file.readlines()):
            if pattern in line:
                penultimate_occurence = index

    return penultimate_occurence
        

def cm_inject_new_definition(text_content: str, filepath: str):
    """ Inject new definition in core-modules.scd """
    index = cm_find_penultimate_occurence(filepath, pattern=");")

    # Looking for the penultimate ); in file, adding right after it

    # Reading file into memory
    with open(filepath, "r") as f:
        contents = f.readlines()

    # injecting new definition
    contents.insert(index-1, text_content)

    # Writing definition to file
    with open(filepath, "w") as f:
        contents = "".join(contents)
        f.write(contents)

    return True

"""
 / \-----------------, 
 \_,|                | 
    |    BootTidal   | 
    |  ,---------------
    \_/______________/ 
"""

def get_boottidal_filepath(filename:str ='BootTidal.hs'):
    """ 
    Return the filepath of BootTidal.hs. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

    

def bt_placeholder_filler(synth_name: str, argument_list: list):
    """ Inserting arguments in placeholder SynthDef """
    template = '''\n:{{\nlet {parameters}
    \n:}}\n'''
    
    
    #if Param1 in json is int make 
   # if type(x) == int :
    #    parameters = ["{x} = pI {x}".format(x=x) for x argument_list]
    
    #and if Param1 in json is float make 
    # elif type(x) == float :
                                #but dont know yet how to acces json, but soon i hope
    parameters = ["{x} = pF {x}".format(x=x) for x in argument_list]
    # weird formatting to match default file
    parameters = "\n     ".join(parameters)
    parameters = parameters.replace('"', '')
    return template.format(synth_name=synth_name, 
            parameters=parameters)

def bt_find_penultimate_occurence(filepath: str, pattern: str):
    """ Find the penultimate occurence of pattern in file and return line """
    penultimate_occurence = 0

    with open(filepath, 'r') as file:
        for index, line in enumerate(file.readlines()):
            if pattern in line:
                penultimate_occurence = index

    return penultimate_occurence
        

def bt_inject_new_definition(text_content: str, filepath: str):
    """ Inject new definition in boottidal """
    index = bt_find_penultimate_occurence(filepath, pattern=":}")

    # Looking for the penultimate ); in file, adding right after it

    # Reading file into memory
    with open(filepath, "r") as f:
        contents = f.readlines()

    # injecting new definition
    contents.insert(index+1, text_content)

    # Writing definition to file
    with open(filepath, "w") as f:
        contents = "".join(contents)
        f.write(contents)

    return True



if __name__ == "__main__":
    
    
#coresynth
    
    cs_FILEPATH = get_coresynths_filepath()
    cs_find_last_occurence(filepath=cs_FILEPATH, pattern="add;")
    new_def = cs_placeholder_filler(synth_name =  my_name,
              nb_inputs = my_inputs,                  
              argument_list = ["param1","param2","param3","param4","param5"])
    cs_inject_new_definition(text_content=new_def, filepath=cs_FILEPATH)

#coremodules

    cm_FILEPATH = get_coremodules_filepath()
    cm_find_penultimate_occurence(filepath=cm_FILEPATH, pattern=");")
    new_def = cm_placeholder_filler(synth_name = my_name,
              argument_list = ["param1","param2","param3","param4","param5"])
    cm_inject_new_definition(text_content=new_def, filepath=cm_FILEPATH)

#boottidal 
    bt_FILEPATH = get_boottidal_filepath()
    bt_find_penultimate_occurence(filepath=bt_FILEPATH, pattern="add;")
    new_def = bt_placeholder_filler(synth_name = my_name,
              argument_list = ["param1","param2","param3","param4","param5"])
    bt_inject_new_definition(text_content=new_def, filepath=bt_FILEPATH)
