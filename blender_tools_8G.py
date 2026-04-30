bl_info = {
    "name": "8G Addon",
    "author": "Sharuk Singh",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar",
    "category": "3D View",
}

import bpy
import colorsys

def update_preview(self, context):
    r, g, b = colorsys.hsv_to_rgb(
        self.sheen_rim_hue,
        self.sheen_rim_saturation,
        self.sheen_rim_value
    )
    self.sheen_rim_preview = (r, g, b)

def register_properties():
    bpy.types.Scene.sheen_rim_sheen = bpy.props.FloatProperty(
        name="Sheen",
        default=0.5,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_roughness = bpy.props.FloatProperty(
        name="Roughness",
        default=0.2,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_hue = bpy.props.FloatProperty(
        name="Hue",
        default=0.0,
        min=0.0,
        max=1.0,
        update=update_preview
    )

    bpy.types.Scene.sheen_rim_saturation = bpy.props.FloatProperty(
        name="Saturation",
        default=0.0,
        min=0.0,
        max=1.0,
        update=update_preview
    )

    bpy.types.Scene.sheen_rim_value = bpy.props.FloatProperty(
        name="Value",
        default=5,
        min=0.0,
        update=update_preview
    )

    bpy.types.Scene.sheen_rim_preview = bpy.props.FloatVectorProperty(
        name="Preview",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0
    )


def unregister_properties():
    del bpy.types.Scene.sheen_rim_sheen
    del bpy.types.Scene.sheen_rim_roughness
    del bpy.types.Scene.sheen_rim_hue
    del bpy.types.Scene.sheen_rim_saturation
    del bpy.types.Scene.sheen_rim_value
    del bpy.types.Scene.sheen_rim_preview


for cls in list(bpy.types.Operator.__subclasses__()):
    if "SHEEN_RIM" in cls.__name__:
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass

# ------------------------
# Operator (does nothing yet)
# ------------------------
class SHEEN_RIM_OT_button(bpy.types.Operator):
    bl_idname = "sheen_rim.button"
    bl_label = "Sheen Rim"
    bl_description = "Add sheen rim to selected objects."

    def execute(self, context):

        # ---- Check selection ----
        selected = context.selected_objects

        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        applied_count = 0

        for obj in selected:

            # Skip non-mesh objects (optional but safer)
            if obj.type != 'MESH':
                continue

            mat = obj.active_material

            if mat is None:
                continue

            if not mat.use_nodes:
                continue

            nodes = mat.node_tree.nodes

            # ---- Find Principled BSDF ----
            principled = None
            for node in nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    principled = node
                    break

            if principled is None:
                continue

            scene = context.scene

            h = scene.sheen_rim_hue
            s = scene.sheen_rim_saturation
            v = scene.sheen_rim_value

            r, g, b = colorsys.hsv_to_rgb(h, s, v)

            sheen_val = scene.sheen_rim_sheen
            roughness_val = scene.sheen_rim_roughness
            tint = scene.sheen_rim_value

            if "Sheen Weight" in principled.inputs:
                principled.inputs["Sheen Weight"].default_value = sheen_val
            elif "Sheen" in principled.inputs:
                principled.inputs["Sheen"].default_value = sheen_val

            if "Sheen Roughness" in principled.inputs:
                principled.inputs["Sheen Roughness"].default_value = roughness_val

            if "Sheen Tint" in principled.inputs:
                principled.inputs["Sheen Tint"].default_value = (r, g, b, 1.0)
            
            applied_count += 1

        # ---- Feedback ----
        if applied_count == 0:
            self.report({'WARNING'}, "No valid materials found")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Sheen Rim applied to {applied_count} object(s)")
        return {'FINISHED'}


class SHEEN_RIM_OT_reset(bpy.types.Operator):
    bl_idname = "sheen_rim.reset"
    bl_label = "Reset Values"
    bl_description = "Reset sheen rim settings to default"

    def execute(self, context):
        scene = context.scene

        scene.sheen_rim_sheen = 0.5
        scene.sheen_rim_roughness = 0.2
        scene.sheen_rim_hue = 0.0
        scene.sheen_rim_saturation = 0.0
        scene.sheen_rim_value = 5

        self.report({'INFO'}, "Sheen Rim values reset")
        return {'FINISHED'}


# ------------------------
# Panel
# ------------------------
class SHEEN_RIM_PT_panel(bpy.types.Panel):
    bl_label = "Shader Helpers"
    bl_idname = "8G_TOOLS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "8G Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Sheen Rim Settings")

        layout.prop(scene, "sheen_rim_sheen")
        layout.prop(scene, "sheen_rim_roughness")
        
        layout.label(text="Tint (HSV)")
        row = layout.row(align=True)
        row.prop(scene, "sheen_rim_hue", text="H")
        row.prop(scene, "sheen_rim_saturation", text="S")
        row.prop(scene, "sheen_rim_value", text="V")
        
        row = layout.row()
        row.enabled = False
        row.prop(scene, "sheen_rim_preview", text="Sheen color")

        layout.separator()

        layout.operator("sheen_rim.reset", icon='LOOP_BACK')
        layout.operator("sheen_rim.button", icon='SHADING_RENDERED')


# ------------------------
# Register
# ------------------------
classes = (
    SHEEN_RIM_OT_button,
    SHEEN_RIM_OT_reset,
    SHEEN_RIM_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_properties()


if __name__ == "__main__":
    register()