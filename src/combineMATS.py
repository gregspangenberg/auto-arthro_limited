from Directory import models_dict, intact

for model_name in models_dict:
    a = mdb.models[model_name].rootAssembly
    
    # remove all instances in assembly
    for item in a.instances.keys():
        del a.features[item]

        # Create instances for parts to be combined
        cort = models_dict[model_name]['cort']
        if model_name.startswith(intact):
            trab = models_dict[model_name]['trab_mat']
            p = mdb.models[model_name].parts[cort]
            a.Instance(name=cort+'-1', part=p, dependent=ON)

            p = mdb.models[model_name].parts[trab]
            a.Instance(name=trab+'-1', part=p, dependent=ON)
        
        else:
            trab = models_dict[model_name]['trab_cut_mat']
            p = mdb.models[model_name].parts[cort]
            a.Instance(name=cort+'-1', part=p, dependent=ON)
            
            p = mdb.models[model_name].parts[trab]
            a.Instance(name=trab+'-1', part=p, dependent=ON)
        
        a.InstanceFromBooleanMerge(name=models_dict[model_name]['bone'], instances=(
            a.instances[cort+'-1'], a.instances[trab+'-1'], ), 
            keepIntersections=ON, originalInstances=SUPPRESS, mergeNodes=BOUNDARY_ONLY, 
            nodeMergingTolerance=1e-06, domain=BOTH)
