import bpy
import bmesh
import numpy as np
import open3d as o3d
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.blender.workflows import select_object
from meshemy.utility.io import o3d_from_vertices_faces


def load_mesh_from_o3d(open3d_triangular_mesh: o3d.geometry.TriangleMesh, name: str = "new_object"):
    # https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/
    new_mesh = bpy.data.meshes.new("new_mesh")
    new_mesh.from_pydata(
        np.asarray(open3d_triangular_mesh.vertices),
        (),
        np.asarray(open3d_triangular_mesh.triangles),
    )
    new_mesh.update()

    # make object from mesh
    new_object = bpy.data.objects.new(name, new_mesh)

    # make collection
    new_collection = bpy.data.collections.new("new_collection")
    bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    new_collection.objects.link(new_object)

    return new_object


def vertices_and_faces(mesh_object_name: str) -> tuple[NDArrayFp64, NDArray]:
    _ob = select_object(mesh_object_name)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY")
    bpy.ops.object.mode_set(mode="OBJECT")

    bm = bmesh.new()
    bm.from_mesh(select_object(mesh_object_name).data)

    return (
        np.array([v.co.copy() for v in bm.verts], dtype=np.float64),
        np.array([[v.index for v in f.verts] for f in bm.faces])
    )


def load_mesh_to_o3d(mesh_object_name: str) -> o3d.geometry.TriangleMesh:
    return o3d_from_vertices_faces(*vertices_and_faces(mesh_object_name))
