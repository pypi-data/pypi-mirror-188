from typing import Optional, Any

import bpy


def empty_scene():
    bpy.ops.scene.new(type="EMPTY")


def select_object(name: str):
    ob = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
    bpy.context.view_layer.objects.active = ob  # Make the cube the active object
    ob.select_set(True)
    return ob


def select_one_or_all(name: Optional[str] = None) -> Any:
    if name:
        return select_object(name)
    bpy.ops.mesh.select_all(action='SELECT')
