from Directory import model_comb, working_directory_path, meshwash_path, model_wash, mats_path, intact, models_dict
import os

def export_inp(model_comb, meshwash_path, working_directory_path, models_dict):
    os.chdir(meshwash_path)

    for part_to_wash in models_dict:
        a = mdb.models[model_comb].rootAssembly
        p = mdb.models[model_comb].parts[part_to_wash]
        a.Instance(name = part_to_wash +'-1', part=p, dependent=ON)
        mdb.Job(name = part_to_wash, model = model_comb, description='', 
            type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
            memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
            numCpus=1, numGPUs=0)

        mdb.jobs[part_to_wash].writeInput(consistencyChecking=OFF)
        a.features[part_to_wash+'-1'].suppress()
    
    os.chdir(working_directory_path)

def import_inp(meshwash_path, working_directory_path, model_wash, models_dict):
    mdb.Model(name = model_wash, modelType=STANDARD_EXPLICIT)
    os.chdir(meshwash_path)

    for part_to_wash in models_dict:
        mdb.ModelFromInputFile(name=part_to_wash, inputFileName=meshwash_path+'\\'+part_to_wash+'.inp')
        mdb.models[model_wash].Part(part_to_wash, mdb.models[part_to_wash].parts[part_to_wash.upper()]) # For some reason Abaqus reimports the part with all uppercase letters upper() is needed to reference
        del mdb.models[part_to_wash]
        
    os.chdir(working_directory_path)

def resection(model_wash, models_dict):
    from itertools import ifilterfalse
    
    for model_to_resect in models_dict:
        #Find name of sets within part in model_wash model
        Sets = mdb.models[model_wash].parts[model_to_resect].sets.keys()
        Sets = [Set.title() for Set in Sets]

        #Change set names from caps to title
        for Set in Sets:
            mdb.models[model_wash].parts[model_to_resect].sets.changeKey(
                fromName = Set.upper(), toName=Set)
        
        #Create a new model for the part 
        mdb.Model(name = model_to_resect, modelType=STANDARD_EXPLICIT)
        
        for Set in Sets:
            #Create a part for the set
            mdb.models[model_to_resect].Part(name=Set, objectToCopy=mdb.models[model_wash].parts[model_to_resect])
            
            #Delete all unassociated sets and elements 
            NotSets = list(ifilterfalse(lambda x: x == Set, Sets))
            for NotSet in NotSets:
                p = mdb.models[model_to_resect].parts[Set]
                p.deleteElement(elements=p.sets[NotSet], deleteUnreferencedNodes=ON) #unknown key error Cort_Bot_011L
                del mdb.models[model_to_resect].parts[Set].sets[NotSet]

def bone_mat_inp(mats_path, working_directory_path, models_dict):
    os.chdir(mats_path)
    
    for bone_mat_model in models_dict:
        try:
            bone_mat_part = models_dict[bone_mat_model]['trab_cut']
        except:
            bone_mat_part = models_dict[bone_mat_model]['trab']
        
        try:
            a = mdb.models[bone_mat_model].rootAssembly
            a.DatumCsysByDefault(CARTESIAN)
            p = mdb.models[bone_mat_model].parts[bone_mat_part]
            a.Instance(name= bone_mat_part+'-1', part=p, dependent=ON)
            mdb.Job(name=bone_mat_part, model=bone_mat_model, description='', type=ANALYSIS, 
                atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
                memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
                explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
                modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
                scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
                numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
                numCpus=1, numGPUs=0)
            mdb.jobs[bone_mat_part].writeInput(consistencyChecking=OFF)
            a.features[bone_mat_part+'-1'].suppress()
        
        except:
            '''
            Occasionally an implant will fail because it cannot be meshed properly.
            failsafe() redoes the meshing and uses virtual topology for the sample that 
            did not mesh properly.
            '''

            failsafe(bone_mat_model)

            a = mdb.models[bone_mat_model].rootAssembly
            a.DatumCsysByDefault(CARTESIAN)
            p = mdb.models[bone_mat_model].parts[bone_mat_part]
            a.Instance(name= bone_mat_part+'-1', part=p, dependent=ON)
            mdb.Job(name=bone_mat_part, model=bone_mat_model, description='', type=ANALYSIS, 
                atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
                memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
                explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
                modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
                scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
                numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
                numCpus=1, numGPUs=0)
            mdb.jobs[bone_mat_part].writeInput(consistencyChecking=OFF)
            a.features[bone_mat_part+'-1'].suppress()

    os.chdir(working_directory_path)         

def failsafe(failed):
    '''
    This is a brute force approach to solving bad meshes.
    Ideally i would like to get some data from abaqus about which parts
    do and dont have meshes and then decide on using virtual topology.
    '''
   # Virtual Topology #
    p = mdb.models[model_comb].parts[failed]
    p.createVirtualTopology(mergeShortEdges=True, shortEdgeThreshold=0.2, 
        mergeSmallFaces=True, smallFaceAreaThreshold=0.2, mergeSliverFaces=False, 
        mergeSmallAngleFaces=True, smallFaceCornerAngleThreshold=10.0, 
        mergeThinStairFaces=True, thinStairFaceThreshold=0.05, 
        ignoreRedundantEntities=True, cornerAngleTolerance=30.0, 
        applyBlendControls=True, blendSubtendedAngleTolerance=60.0, 
        blendRadiusTolerance=1.4)
                                        
    # Mesh Generation #
    p = mdb.models[model_comb].parts[failed]
    c = p.cells
    high,low=c.getBoundingBox().values()
    lx,ly,lz=low
    hx,hy,hz=high
    region=c.getByBoundingBox(lx,ly,lz,hx,hy,hz)

    p.seedPart(size=1.2, deviationFactor=0.05, minSizeFactor=0.01)
    p.setMeshControls(regions=region, elemShape=TET, technique=FREE,allowMapped=True)
    elemType1=mesh.ElemType(elemCode=C3D10, elemLibrary= STANDARD)
    p.setElementType(regions=(region,), elemTypes=(elemType1,))

    p.generateMesh()
    print('Mesh generated for '+ failed)

    # Export INP #
    os.chdir(meshwash_path)
    a = mdb.models[model_comb].rootAssembly
    p = mdb.models[model_comb].parts[failed]
    a.Instance(name = failed +'-1', part=p, dependent=ON)
    mdb.Job(name = failed, model = model_comb, description='', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
        numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
        numCpus=1, numGPUs=0)
    mdb.jobs[failed].writeInput(consistencyChecking=OFF)
    a.features[failed+'-1'].suppress()
    os.chdir(working_directory_path)

    # Import INP #
    mdb.Model(name = model_wash, modelType=STANDARD_EXPLICIT)
    os.chdir(meshwash_path)

    mdb.ModelFromInputFile(name=failed, inputFileName=meshwash_path+'\\'+failed+'.inp')
    mdb.models[model_wash].Part(failed, mdb.models[failed].parts[failed.upper()]) # For some reason Abaqus reimports the part with all uppercase letters upper() is needed to reference
    del mdb.models[failed]
        
    os.chdir(working_directory_path)

    # Resectioning #
    from itertools import ifilterfalse
    
    #Find name of sets within part in model_wash model
    Sets = mdb.models[model_wash].parts[failed].sets.keys()
    Sets = [Set.title() for Set in Sets]

    #Change set names from caps to title
    for Set in Sets:
        mdb.models[model_wash].parts[failed].sets.changeKey(
            fromName = Set.upper(), toName=Set)
    
    #Create a new model for the part 
    mdb.Model(name = failed, modelType=STANDARD_EXPLICIT)
    
    for Set in Sets:
        #Create a part for the set
        mdb.models[failed].Part(name=Set, objectToCopy=mdb.models[model_wash].parts[failed])
        
        #Delete all unassociated sets and elements 
        NotSets = list(ifilterfalse(lambda x: x == Set, Sets))
        for NotSet in NotSets:
            p = mdb.models[failed].parts[Set]
            p.deleteElement(elements=p.sets[NotSet], deleteUnreferencedNodes=ON) #unknown key error Cort_Bot_011L
            del mdb.models[failed].parts[Set].sets[NotSet]


#Define the objects to be worked upon    

export_inp(model_comb, meshwash_path, working_directory_path, models_dict)
import_inp(meshwash_path, working_directory_path, model_wash, models_dict)
resection(model_wash, models_dict)
bone_mat_inp(mats_path, working_directory_path, models_dict)

