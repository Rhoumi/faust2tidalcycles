import os
import sys
import os.path
from os import path
import json
from collections import ChainMap
import subprocess
import platform
import shutil

def get_coresynths_filepath(filename:str ='core-synths.scd'):
    """ 
    Return the filepath of core-synths.scd. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

 

def placeholder_filler(synth_name: str, nb_inputs : int, argument_list: list):
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

def find_last_occurence(filepath: str, pattern: str):
    """ Find the last occurence of pattern in file and return line """
    last_occurence = 0

    with open(filepath, 'r') as file:
        for index, line in enumerate(file.readlines()):
            if pattern in line:
                last_occurence = index

    return last_occurence
        

def inject_new_definition(text_content: str, filepath: str):
    """ Inject new definition in core-synths.scd """
    index = find_last_occurence(filepath, pattern=".add;")

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

if __name__ == "__main__":
    FILEPATH = get_coresynths_filepath()
    find_last_occurence(filepath=FILEPATH, pattern="add;")
    new_def = placeholder_filler(synth_name =  "FAUSTDSP",
              nb_inputs = 2,                  
              argument_list = ["param1","param2","param3","param4","param5"])
    inject_new_definition(text_content=new_def, filepath=FILEPATH)
