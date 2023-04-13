import open3d as o3d
import pyassimp
import trimeshExtract
import numpy as np
import os


def convert_to_open3d_mesh(mesh):
    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

    if hasattr(mesh, 'vertex_colors') and mesh.vertex_colors:
        o3d_mesh.vertex_colors = o3d.utility.Vector3dVector(mesh.vertex_colors)

    if hasattr(mesh, 'normals') and mesh.normals:
        o3d_mesh.vertex_normals = o3d.utility.Vector3dVector(mesh.normals)

    return o3d_mesh


def convert_to_trimesh(mesh):
    trimesh_mesh = trimeshExtract.Trimesh(vertices=np.asarray(mesh.vertices), faces=np.asarray(mesh.triangles))

    if mesh.has_vertex_normals():
        trimesh_mesh.vertex_normals = np.asarray(mesh.vertex_normals)

    if mesh.has_vertex_colors():
        trimesh_mesh.vertex_colors = np.asarray(mesh.vertex_colors) * 255

    return trimesh_mesh


def extract_meshes_from_fbx_file(fbx_file):
    scene = pyassimp.load(fbx_file)
    meshes = []

    for mesh in scene.meshes:
        o3d_mesh = convert_to_open3d_mesh(mesh)
        meshes.append(o3d_mesh)

    pyassimp.release(scene)
    return meshes


def save_mesh_as_glb(mesh, output_file):
    glb_data = mesh.export(file_type='glb')
    with open(output_file, 'wb') as f:
        f.write(glb_data)


def main():
    fbx_file = 'Box.fbx'
    meshes = extract_meshes_from_fbx_file(fbx_file)

    output_dir = 'output_meshes'
    os.makedirs(output_dir, exist_ok=True)

    for i, mesh in enumerate(meshes):
        trimesh_mesh = convert_to_trimesh(mesh)
        output_file = os.path.join(output_dir, f'output_mesh_{i}.glb')
        save_mesh_as_glb(trimesh_mesh, output_file)
        print(f'Saved mesh {i} to {output_file}')


if __name__ == '__main__':
    main()
