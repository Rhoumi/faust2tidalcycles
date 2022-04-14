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

# Opening JSON file
with open('/home/ralt144mi/Documents/GRAME/TESTPY/testeffet.dsp.json') as json_file:
    json_data = json.load(json_file)
#with open('testvgroup.dsp.json','r') as string:
 #   json_data_string = json.load(string)
  #  string.close()
    
  #  print(json_data_string)
 
    # Print the type of data variable
  #  print("Type:", type(json_data))
 
    # Print the data of dictionary
    
    my_inputs = json_data['inputs']
    my_outputs = json_data['outputs']
    my_name = json_data['name']

    
    
    addresses = ''
    

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
def get_header_paths(headerpath):
    folders = [
        path.join(headerpath, "plugin_interface"),
        path.join(headerpath, "server"),
        path.join(headerpath, "common")
    ]

    if all(path.exists(folder) for folder in folders):
        print("Found SuperCollider headers: %s" % headerpath)
        return folders

# Try and find SuperCollider headers on system
def find_headers(headerpath):
    folders = get_header_paths(headerpath)
    if folders:
        return folders

    # Possible locations of SuperCollider headers
    guess = [
        "/usr/local/include/SuperCollider",
        "/usr/local/include/supercollider",
        "/usr/include/SuperCollider",
        "/usr/include/supercollider",
        "/usr/local/include/SuperCollider/",
        "/usr/share/supercollider-headers",
        path.join(os.getcwd(), "supercollider")
    ]

    if 'HOME' in os.environ:
        guess.append(path.join(os.environ['HOME'], "supercollider"))

    for headerpath in guess:
        folders = get_header_paths(headerpath)
        if folders:
            return folders

    sys.exit("Could not find SuperCollider headers")

    
find_headers("./include")

def find_file(file_name, directory_name):
    files_found = []
    for path, subdirs, files in os.walk(directory_name):
        for name in files:
            if(file_name == name):
                file_path = os.path.join(path,name)
                files_found.append(file_path)
    return files_found


cs_loc = ''.join(find_file('core-synths.scd', '/home/ralt144mi/.local/share/SuperCollider'))
cm_loc = ''.join(find_file('core-modules.scd', '/home/ralt144mi/.local/share/SuperCollider'))
bt_loc = ''.join(find_file('BootTidal.hs', '/home/ralt144mi/.cabal/share'))

print(cs_loc)
print(cm_loc)
print(bt_loc)

    
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
        | out, {in_list},{argument_list}|
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
    parameters = ['{x} = pF ""{x}""'.format(x=x) for x in argument_list]
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
    
#json

    json_data = json_to_ui_data(json_data)
    param = parameter_gatherer(json_data)
    param = list(flatten(param))
    print(param)
    
        
#coresynth
    
   # cs_FILEPATH = get_coresynths_filepath()
    cs_FILEPATH = cs_loc
    cs_find_last_occurence(filepath=cs_FILEPATH, pattern="add;")
    new_def = cs_placeholder_filler(synth_name =  my_name,
              nb_inputs = my_inputs,                  
              argument_list = param)
    cs_inject_new_definition(text_content=new_def, filepath=cs_FILEPATH)

#coremodules

    #cm_FILEPATH = get_coremodules_filepath()
    cm_FILEPATH = cm_loc
    cm_find_penultimate_occurence(filepath=cm_FILEPATH, pattern=");")
    new_def = cm_placeholder_filler(synth_name = my_name,
              argument_list = param)
    cm_inject_new_definition(text_content=new_def, filepath=cm_FILEPATH)

#boottidal 

    #bt_FILEPATH = get_boottidal_filepath()
    bt_FILEPATH = bt_loc
    bt_find_penultimate_occurence(filepath=bt_FILEPATH, pattern="add;")
    new_def = bt_placeholder_filler(synth_name = my_name,
              argument_list = param)
    bt_inject_new_definition(text_content=new_def, filepath=bt_FILEPATH)
