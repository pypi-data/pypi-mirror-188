from pathlib import Path

import numpy as np
from pydantic import BaseModel
import open3d as o3d
from pydantic_numpy import NDArray


class Open3dCookbook(BaseModel):
    mesh: o3d.geometry.TriangleMesh

    class Config:
        arbitrary_types_allowed = True

    def smoothen(self, iterations: int, copy: bool = False) -> None:
        result = self.mesh.filter_smooth_taubin(number_of_iterations=iterations)
        if copy:
            self.__class__(mesh=result)
        self.mesh = result

    @property
    def vertices(self) -> NDArray:
        return np.asarray(self.mesh.vertices)

    @property
    def faces(self) -> NDArray:
        return np.asarray(self.mesh.triangles)

    @property
    def triangles(self) -> NDArray:
        return self.faces

    def save_glb(self, path: Path) -> None:
        open3d_triangular_mesh = (
            self.mesh.remove_duplicated_triangles()
            .remove_duplicated_vertices()
            .remove_degenerate_triangles()
            .remove_unreferenced_vertices()
        )
        o3d.io.write_triangle_mesh(
            str(path.with_suffix(".glb")),
            open3d_triangular_mesh,
            write_vertex_colors=False,
            write_triangle_uvs=False,
        )
