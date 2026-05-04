import bpy
import colorsys

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

        if applied_count == 0:
            self.report({'WARNING'}, "No valid materials found")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Sheen Rim applied to {applied_count} object(s)")
        return {'FINISHED'}