from pydantic import BaseModel, FilePath
import open3d as o3d

from meshemy.blender.constant import SUFFIX_TO_READER
from meshemy.blender.utils import load_mesh_from_o3d, load_mesh_to_o3d, vertices_and_faces
from meshemy.blender.workflows import select_object, planar_decimate_mesh, merge_close
from meshemy.utility.io import o3d_from_vertices_faces
from meshemy.utility.seal import seal_mesh


class BlenderCookbook(BaseModel):
    mesh_name: str

    def bpy_select(self) -> None:
        select_object(self.mesh_name)

    def planar_decimate(self, degree_tol: float) -> None:
        planar_decimate_mesh(degree_tol, mesh_object_name=self.mesh_name)

    def merge_close(self, distance_tol: float) -> None:
        return merge_close(distance_tol, mesh_object_name=self.mesh_name)

    def to_o3d(self, attempt_seal_insurance: bool = True) -> o3d.geometry.TriangleMesh:
        vertices, faces = vertices_and_faces(mesh_object_name=self.mesh_name)
        if attempt_seal_insurance:
            vertices, faces = seal_mesh(vertices, faces)
        return o3d_from_vertices_faces(vertices, faces)

    @classmethod
    def from_o3d(cls, *, mesh: o3d.geometry.TriangleMesh, name: str) -> "Meshemist":
        _ob = load_mesh_from_o3d(mesh, name)
        return cls(mesh_name=name)

    @classmethod
    def from_file(cls, path: FilePath, *args, **kwargs) -> "Meshemist":
        SUFFIX_TO_READER[path.suffix](*args, **kwargs)


