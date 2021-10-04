# auto-arthro_limited

This code is a simplified version of auto-arthro which allows for easy setup of abaqus simulations
of implanted bones. 

Begin by setting up a python 2.7 development environment and install the only required library
pathlib2. Run Directory.py and type in the name of the folder to be created when prompted. This
will create a folder of the inputted name with 4 sub-folders named:
- Import
- MATS
- MeshWash
- Work

Place your cortical and trabecular bone files as .sldprt in Import and your implants as .step in Import.
Then run CONTROLLER.py and indicate you are on step 1 when queried. Apply material properties to the
trabecular bones outputted to MATS and add the suffix 'MATS' to the end of each file with material 
properties. Run CONTROLLER.py again and indicate you are on step 2. 

You now have an implanted bone with material properties that has been meshed and is ready for loads,
boundary conditions etc. to be applied!
