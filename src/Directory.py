#Copyright 2020, Gregory Spangeberg, All rights reserved.
"""
Create Dictionary of Files and Paths
-the repository mdb.models['Model-1'].parts contains information of 
the parts within each Model
-this script should only be for importing after use the above repository

"""
import os
import sys

# When within abaqus
try:
    sample=sys.argv[-1]   #ex. 011L
    root_path=sys.argv[-2]    

# Outside abaqus, change sample to create new folder structure
except:
    sample = '011L' # Specify name of folder to be created
    root_path = os.getcwd()

# Names of Subfolders
working_directory_path = root_path + '/Sample/'+sample +'/Work/' 
meshwash_path = root_path + '/Sample/'+sample +'/MeshWash/'
mats_path = root_path + '/Sample/'+sample +'/MATS/'
import_path = root_path + '/Sample/'+sample +'/Import/'
inp_path = root_path + '/Sample/'+sample +'/MATS/'

# When module is run by itself it creates the directory strucutre it will later need
if __name__ == '__main__':
    import pathlib2
    paths = [locals()[path] for path in locals().keys() if path.endswith('path')]
    for path in paths:
        pathlib2.Path(path).mkdir(parents=True, exist_ok=True)

# When the module is imported or used in abaqus, the following block of code is executed
else:
    folder_files = os.listdir(import_path)
    file_path = []
    for item in folder_files:
        file_path.append(import_path+item)

    '''The following code defines the naming convention for the study.
    By default the name of the files in the imported folder will be identical to 
    the ones in the simulation.

    A dictionary is also created that outlines the naming of the final models
    and their constituent parts. The dictionary should be used instead of calling mdb.....keys()
    '''
    #Create list of variables and inserts '_' into whitespace and removes any 'cut' word
    var_list = [os.path.splitext(item)[0]\
    .title().replace(' ','_').replace('_Cut','') for item in folder_files]
    bone_list = [var for var in var_list if var.startswith(('Cort','Trab'))]
    cort_name = [bone for bone in bone_list if bone.startswith('Cort')][0]
    trab_name = [bone for bone in bone_list if bone.startswith('Trab')][0]
    implant_list = list(set(var_list) - set(bone_list))

    #Create Dictionary of variables and their file paths
    file_path_dict = dict(zip(var_list,file_path))

    # Names of the intermediate models, which are denoted by an 'x' prefix
    model_import = 'xImported'
    model_comb = 'xCombined'
    model_wash = 'xWash'

    # Define the name for the unmodified reference bone
    intact = 'Intact'

    # Which samples should use virtual topology
    # virtual_topology_samples = 

    # Create the naming scheme for this study
    #Trab_Bot everythin else is Trab-Implantname , fix this!
    model_list =  implant_list + [intact+'_'+sample]
    models_dict = {}
    for model in model_list:
        models_dict[model] = {}
        models_dict[model]['cort'] = cort_name
        models_dict[model]['trab'] = trab_name
        models_dict[model]['bone'] = 'Bone-' + model   # name of comvined cort and trab
        if model not in implant_list:
            models_dict[model]['trab_mat'] = trab_name + 'MAT' #unchangeable MAT prefix must be applied
        if model in implant_list:
            models_dict[model]['trab_cut'] = 'Trab-' + model
            models_dict[model]['trab_cut_mat'] = 'Trab-' + model + 'MAT' #unchangeable
            models_dict[model]['implant'] = 'Implant-' + model
            
