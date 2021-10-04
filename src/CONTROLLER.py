#Copyright 2020, Gregory Spangeberg, All rights reserved.

#Run the Abaqus script
import os
import shutil
from Directory import inp_path, meshwash_path
################################################################################
'''
Run Directory and change sample = ' ' to your sample name to create the diurectory structure 
''' 
 
root_path = os.getcwd()


# comment out the section that is not needed

# PART ONE
############################
while True:
            step_num = input('Step 1 or 2? (1/2): ')
            if step_num == '' or not step_num in [1,2]:
                print('invalid')
            else:
                break
if step_num == 1:
    for sample in os.listdir(r'./Sample'):
        if len(os.listdir('Sample/'+sample+'/Import')) == 0: # skip samples with no files
            continue

        working_directory_path =r'./Sample/'+sample+r'/Work/'
        shutil.copy(root_path +'/src/Directory.py', working_directory_path)
        os.chdir(working_directory_path)

        #Start Abaqus and execute the script
        os.system('abaqus cae script='+ root_path +'/src/ExecuteScripts1.py'
            +' -- '+ root_path +' '+ sample)
        os.chdir(root_path)


elif step_num == 2:
    # PART TWO
    ############################
    # Keep only output MAT files in MATS folder move inputs to MeshWash folder
    mats_folder=os.listdir(inp_path)
    for mats_file in mats_folder:
        if mats_file.split('.')[0].endswith('MAT'):
            continue
        else:
            shutil.move(inp_path+ mats_file, 
                meshwash_path+ mats_file)

    #Start Abaqus and execute the script
    for sample in os.listdir(r'./Sample'):
        if len(os.listdir('./Sample/'+sample+'/Work')) == 0: # skip samples with no files
            continue

        working_directory_path =r'./Sample/'+sample+r'/Work/'
        shutil.copy(root_path +'/src/Directory.py', working_directory_path)
        os.chdir(working_directory_path)

        cae_path = root_path + '/Sample/' +sample+'/Work/' +sample+'.cae'
        os.system('abaqus cae script='+ root_path +'/src/ExecuteScripts2.py'
            +' -- '+ cae_path +' '+ root_path +' '+sample)
        
        os.chdir(root_path)
        
else:
    print('error')


