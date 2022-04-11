import os

def get_coremodules_filepath(filename:str ='BootTidal.hs'):
    """ 
    Return the filepath of BootTidal.hs. 
    /!\ This function does not work in interactive mode!
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)

    

def placeholder_filler(synth_name: str, argument_list: list):
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

def find_penultimate_occurence(filepath: str, pattern: str):
    """ Find the penultimate occurence of pattern in file and return line """
    penultimate_occurence = 0

    with open(filepath, 'r') as file:
        for index, line in enumerate(file.readlines()):
            if pattern in line:
                penultimate_occurence = index

    return penultimate_occurence
        

def inject_new_definition(text_content: str, filepath: str):
    """ Inject new definition in core-modules.scd """
    index = find_penultimate_occurence(filepath, pattern=":}")

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
    FILEPATH = get_coremodules_filepath()
    find_penultimate_occurence(filepath=FILEPATH, pattern="add;")
    new_def = placeholder_filler(synth_name = "blabla",
              argument_list = ["param1","param2","param3","param4","param5"])
    inject_new_definition(text_content=new_def, filepath=FILEPATH)
