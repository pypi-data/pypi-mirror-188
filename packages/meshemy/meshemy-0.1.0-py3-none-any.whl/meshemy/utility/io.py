from pydantic_numpy import NDArrayFp64, NDArray
import open3d as o3d


def o3d_from_vertices_faces(vertices: NDArrayFp64, faces: NDArray) -> o3d.geometry.TriangleMesh:
    return o3d.geometry.TriangleMesh(
        o3d.pybind.utility.Vector3dVector(vertices),
        o3d.pybind.utility.Vector3iVector(faces)
    )
