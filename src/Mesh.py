import mesh
import part
from Directory import model_comb 

def MeshComb(model_comb): 
    combined_list= mdb.models[model_comb].parts.keys()

    for combined in combined_list:

        # Virtual Topology
        # if combined in virtual_topology_samples:
        #     p = mdb.models[model_comb].parts[combined]
        #     p.createVirtualTopology(mergeShortEdges=False, mergeSmallFaces=False, 
        #         mergeSliverFaces=False, mergeSmallAngleFaces=True, 
        #         smallFaceCornerAngleThreshold=10.0, mergeThinStairFaces=False, 
        #         ignoreRedundantEntities=False, cornerAngleTolerance=30.0, 
        #         applyBlendControls=False)
                                            
        #Mesh Generation
        p = mdb.models[model_comb].parts[combined]
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
        print('Mesh generated for '+ combined)

MeshComb(model_comb)
