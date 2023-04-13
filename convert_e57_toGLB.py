import open3d as o3d
import numpy as np 
import pandas as pd
import trimesh
from  pye57 import E57
from pyntcloud import PyntCloud

def e57_to_ply(input_file, output_file):
    # Read E57 point cloud    
    e57 = E57(input_file)


    # get point cloud
    data = e57.read_scan(0, intensity=True, colors=True, row_column=True)    

    # Extract point coordinates, colors, and normals
    xyz = np.column_stack((data['cartesianX'], data['cartesianY'], data['cartesianZ']))
    rgb = np.column_stack((data['colorRed'], data['colorGreen'], data['colorBlue']))    

    # Normalize colors to the range [0, 1]
    rgb = rgb / 255.0

    #creaet new point cloud in Open3D library
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors = o3d.utility.Vector3dVector(rgb)

    # Estimate normals
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    # Estimate mesh using Poisson surface reconstruction
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd)

    # Save the mesh as an OBJ file
    temp_obj_file = "temp.obj"
    o3d.io.write_triangle_mesh(temp_obj_file, mesh)


    # Load the OBJ file using trimesh
    trimesh_mesh = trimesh.load_mesh(temp_obj_file)

    # Convert the trimesh mesh to a GLB file
    glb_data = trimesh.exchange.export.export_glb(trimesh_mesh)

    # Save the GLB file
    with open(output_file, 'wb') as f:
        f.write(glb_data)



# end 

# Example usage
input_file = "pump_pointcloud.e57"
output_file = "output_pointcloud.glb"
e57_to_ply(input_file, output_file)
