import os
import sys
import os.path
from os import path
import json
from collections import ChainMap
import subprocess
import platform
import shutil



#JSON#####################

def read_json(json_file):
        f = open(json_file)
        data = json.load(f)
        f.close()
        return data
  #  else:
  #      sys.exit("Could not find json file %s" % json_file)
 #       
# Some parts of the generated json file are parsed as lists of dicts -
# This flattens one of those into one dictionary
def flatten_list_of_dicts(list_of_dicts):
    return ChainMap(*list_of_dicts)

def write_file(file, contents):
    f = open(file, "w")
    f.write(contents)
    f.close()

def make_dir(dir_path):
    if not path.exists(dir_path):
        os.mkdir(dir_path)
        
#####################

def get_coresynths_filepath(filename:str ='core-synths.scd'):
    """ 
    Return the filepath of core-synths.scd. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

 

def placeholder_filler(synth_name: str, argument_list: list):
    """ Inserting arguments in placeholder SynthDef """
    template = '''\n    SynthDef(\"{synth_name}\" ++ ~dirt.numChannels, {{
        | {argument_list}|
        var signal = In.ar(out, ~dirt.numChannels);
        signal = {synth_name}.ar({signal_argument}, out);
        ReplaceOut.ar(out, signal);
         }}).add;
    \n
    '''
    argument_beautify = ', '.join(argument_list)
    return template.format(synth_name=synth_name, 
                           argument_list=argument_beautify,
                           signal_argument=argument_beautify)

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

    # Looking for the last .add in file, adding right after it

    # Reading file into memory
    with open(filepath, "r") as f:
        contents = f.readlines()

    # injecting new definition
    contents.insert(index+1, text_content)

    # Writing definition to file
    with open(filepath, "w") as f:
        contents = "".join(contents)
        f.write(contents)

    return True

def get_parameter_list(json_data, with_initialization):
    out_string = ""
    # The zero index is needed because it's all in the first index, or is it? @FIXME
    counter=0

    inputs = ""
    if json_data["inputs"] > 0:
        for i in range(json_data["inputs"]):
            if i != 0:
                inputs = inputs + ", in%s" % i
            else:
                inputs = inputs + "in%s" % i

    for ui_element in json_data["ui"][0]["items"]:

        param_name=""
        if "label" in ui_element:
            param_name = sanitize_label(ui_element["label"])

        param_default = ""
        if "init" in ui_element:
            param_default = ui_element["init"]
        else:
            param_default = "0"

        # Param name
        if with_initialization:
            this_argument =  "%s(%s)" % (param_name, param_default)
        else:
            this_argument = param_name

        this_argument = this_argument.replace(" ", "_")
        if counter != 0:
            out_string = out_string + ", " + this_argument
        else:
            out_string = this_argument

        counter = counter + 1

    if json_data["inputs"] > 0:
        if out_string == "":
            out_string = inputs
        else:
            out_string = inputs + "," + out_string

    return out_string

# This sanitizes the "name" field from the faust file, makes it capitalized, removes dashes and spaces
def get_class_name(json_data, noprefix):
    # Capitalize all words in string

    name = dsp_name(json_data)

    if noprefix != 1:
        name = "Faust" + name

    # Max length of name is 31
    if len(name) > 31:
        name = name[0:30]

    return name



def normalizeClassName(meta_name):
    upnext=True
    normalized=""
    for char in meta_name:
        if upnext:
            normalized = normalized + char.upper()
            upnext=False
            continue
        if char == "_" or char=="-" or char==" ":
            upnext=True
        else:
            normalized = normalized + char

    maxlen = 31
    return normalized[0:maxlen-1]

def dsp_name(json_data):
    name  = normalizeClassName(json_data["name"])
    return name

if __name__ == "__main__":
    FILEPATH = get_coresynths_filepath()
    find_last_occurence(filepath=FILEPATH, pattern="add;")
    new_def = placeholder_filler(synth_name =  "lol",
            argument_list = ["in", "in2", "out"])
    inject_new_definition(text_content=new_def, filepath=FILEPATH)
