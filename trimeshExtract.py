import trimesh
import os

def extract_meshes_from_glb_file(glb_file):
    loaded_mesh = trimesh.load(glb_file, skip_materials=True)
    if isinstance(loaded_mesh, trimesh.Scene):
        return loaded_mesh.geometry.values()
    else:
        return [loaded_mesh]

def save_mesh_as_glb(mesh, output_file):
    glb_data = mesh.export(file_type='glb')
    with open(output_file, 'wb') as f:
        f.write(glb_data)

def main():
    glb_file = 'BoxAnimated.glb'
    meshes = extract_meshes_from_glb_file(glb_file)

    output_dir = 'output_meshes'
    os.makedirs(output_dir, exist_ok=True)

    for i, mesh in enumerate(meshes):
        output_file = os.path.join(output_dir, f'output_mesh_{i}.glb')
        save_mesh_as_glb(mesh, output_file)
        print(f'Saved mesh {i} to {output_file}')

if __name__ == '__main__':
    main()
