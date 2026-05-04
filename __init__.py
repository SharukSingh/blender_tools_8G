bl_info = {
    "name": "8G Addon",
    "author": "Sharuk Singh",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar",
    "category": "3D View",
}

import bpy

from . import props
from .sheen_rim import operator, panel, reset

classes = (
   	operator.SHEEN_RIM_OT_button,
    reset.SHEEN_RIM_OT_reset,
    panel.SHEEN_RIM_PT_panel,
)

def register():
    props.register_properties()

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    props.unregister_properties()