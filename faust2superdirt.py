import os
import sys
import os.path
from os import path
import json
from collections import ChainMap
import subprocess
import platform
import shutil


######################################
#######▄▄▄#▄▄▄▄▄▄▄#▄▄▄▄▄▄▄#▄▄####▄#### 
######█   █       █       █  █##█ █###
######█   █  ▄▄▄▄▄█   ▄   █   █▄█ █###
###▄##█   █ █▄▄▄▄▄█  █#█  █       █###
##█ █▄█   █▄▄▄▄▄  █  █▄█  █  ▄    █###
##█       █▄▄▄▄▄█ █       █ █#█   █###
##█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█##█▄▄█###
######################################

    
    #####PARAMETERS LISTS
    
    
PARAMETER = ["hslider", "vslider", "hbargraph", "vbarbraph",
                            "nentry", "checkbox", "button"]
GROUP = ["vgroup", "hgroup", "tgroup"]

def flatten(container):
    """ Helper function to flatten arbitrarily nested lists """
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

def json_to_ui_data(json_data: dict):
    """ Return the UI part of the Faust-generated JSON """
    return json_data["ui"][0]

def item_list_processor(items_value: list):
    """ Process data contained in "items" keys """
    parameter_list = []
    # On parcourt chaque dictionnaire que l'on trouve dans la liste "items"
    for items in items_value:
        if isinstance(items, dict):
            # Si on voit que le type correspond à un param, on gagne un param
            if items["type"] in PARAMETER:
                parameter_list.append(items["label"])
            # Sinon, cela signifie que l'on doit 
            # continuer à descendre pour extraire
            elif items["type"] in GROUP:
                parameter_list.append(item_list_processor(items["items"]))
        else:
            pass
    return parameter_list

def parameter_gatherer(data):
    """ JSON Parameter extractor """
    parameter_list = []
    for key, value in data.items():
        if key == "items":
            parameter_list.append(item_list_processor(value))
        else:
            continue
    return parameter_list

    
    
    ###Files Finder

def find_file(file_name, directory_name):
    files_found = []
    for path, subdirs, files in os.walk(directory_name):
        for name in files:
            if(file_name == name):
                file_path = os.path.join(path,name)
                files_found.append(file_path)
    return files_found


#cs_loc = ''.join(find_file('core-synths.scd', '/home/ralt144mi/.local/share/SuperCollider'))
#cm_loc = ''.join(find_file('core-modules.scd', '/home/ralt144mi/.local/share/SuperCollider'))
#bt_loc = ''.join(find_file('BootTidal.hs', '/home/ralt144mi/.cabal/share'))

#print(cs_loc)
#print(cm_loc)
#print(bt_loc)


###END OF WIP ON PATHS..................
    
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

 

def cs_placeholder_filler(synth_name: str, c_synth_name:str, nb_inputs : int, argument_list: list):
    """ Inserting arguments in placeholder SynthDef """
    template = '''\nSynthDef(\"{synth_name}\" ++ ~dirt.numChannels, {{
        | out, {in_list},{argument_list}|
        var signal = In.ar(out, ~dirt.numChannels);
        signal = {c_synth_name}.ar({signal_beg},{signal_argument}, out);
        ReplaceOut.ar(out, signal);
         }}).add;\n
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
                           c_synth_name=c_synth_name,
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
            }} {subparameters} }});
    \n'''
    parameters = ["{x}: ~{x}".format(x=x) for x in argument_list]
    subparameters = [",{{~{x}.notNil".format(x=x) for x in argument_list]
    # weird formatting to match default file
    parameters = ",\n                ".join(parameters)
    subparameters = " or:  ".join(subparameters)
    parameters = parameters.replace('"', '')
    return template.format(synth_name=synth_name, 
            parameters=parameters,
           subparameters=subparameters)

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
    
    
    #FOR THE MOMENT it's only converting parameters to float because it always work
    #but maybe in the future see if its a checkbox or button or something needed to be a int to maybe convert arguments to int ( ... = pI "...." )
    
    
    parameters = [" {x} = pF \"{x}\"  ".format(x=x) for x in argument_list]
    # weird formatting to match default file
    parameters = "\n     ".join(parameters)
    parameters = parameters.replace('', '')
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
    
    
    import argparse
    import sys
    import tempfile

    parser = argparse.ArgumentParser(
        description='Compile faust .dsp files to SuperCollider plugins including class and help files and supernova objects'
    )

    parser.add_argument("inputjson", help="A Faust JSON .dsp.json file to be used, normally created in the same path as your Faust.dsp by faust2sc.py")
    
    parser.add_argument("boottidalloc", help="Your BootTidal.hs path, it's never where you think it is, be carefull")


    # args = parser.parse_args()
    args, unknownargs = parser.parse_known_args()

    # Flatten list of arguments to one string
    unknownargs = " ".join(unknownargs)
    faustflags = unknownargs or ""

    # Temporary folder for intermediary files
    tmp_folder = tempfile.TemporaryDirectory(prefix="faust.")

    #scresult = faust2sc(args.inputfile, tmp_folder.name, noprefix, args.architecture, faustflags)


    
#json

# Opening JSON file

    with open(args.inputjson) as json_file:
        json_data = json.load(json_file)
        my_inputs = json_data['inputs']
        my_outputs = json_data['outputs']
        my_name = json_data['name']

    json_data = json_to_ui_data(json_data)
    param = parameter_gatherer(json_data)
    param = list(flatten(param))
    print("the list of parameters is : ")
    print(param)

    
        
#coresynth
    
   # cs_FILEPATH = get_coresynths_filepath()
    cs_FILEPATH = ''.join(find_file('core-synths.scd', os.environ['HOME']+'/.local/share/SuperCollider'))
    print(cs_FILEPATH)
    cs_find_last_occurence(filepath=cs_FILEPATH, pattern="add;")
    new_def = cs_placeholder_filler(synth_name =  my_name,
              c_synth_name = my_name.capitalize(),
              nb_inputs = my_inputs,                  
              argument_list = param)
    cs_inject_new_definition(text_content=new_def, filepath=cs_FILEPATH)

#coremodules

    #cm_FILEPATH = get_coremodules_filepath()
    cm_FILEPATH = ''.join(find_file('core-modules.scd', os.environ['HOME']+'/.local/share/SuperCollider'))
    print(cm_FILEPATH)
    cm_find_penultimate_occurence(filepath=cm_FILEPATH, pattern=");")
    new_def = cm_placeholder_filler(synth_name = my_name,
              argument_list = param)
    cm_inject_new_definition(text_content=new_def, filepath=cm_FILEPATH)

#boottidal 

    #bt_FILEPATH = get_boottidal_filepath()
    bt_FILEPATH = ''.join(find_file('BootTidal.hs', args.boottidalloc))
    print(bt_FILEPATH)
    bt_find_penultimate_occurence(filepath=bt_FILEPATH, pattern="add;")
    new_def = bt_placeholder_filler(synth_name = my_name,
              argument_list = param)
    bt_inject_new_definition(text_content=new_def, filepath=bt_FILEPATH)
    
