import open3d as o3d
import os

def extract_meshes_from_glb_file(glb_file):
    triangle_meshes = o3d.io.read_triangle_mesh(glb_file)
    return triangle_meshes

def save_mesh_as_glb(mesh, output_file):
    o3d.io.write_triangle_mesh(output_file, mesh, write_triangle_uvs=True, write_triangle_normals=True)

def main():
    glb_file = 'hazlight.glb'
    meshes = extract_meshes_from_glb_file(glb_file)

    output_dir = 'output_meshes'
    os.makedirs(output_dir, exist_ok=True)

    for i, mesh in enumerate(meshes):
        output_file = os.path.join(output_dir, f'output_mesh_{i}.glb')
        save_mesh_as_glb(mesh, output_file)
        print(f'Saved mesh {i} to {output_file}')

if __name__ == '__main__':
    main()
