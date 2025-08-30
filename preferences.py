import os

import bpy
from bpy_extras.io_utils import ImportHelper

from .utils.util import drawMultilineLabel, getPreferences
from .consts import ADDON_NAME

class DirectoryProperty(bpy.types.PropertyGroup):
    directory: bpy.props.StringProperty(name="", subtype='DIR_PATH')

class SelectDirectory(bpy.types.Operator, ImportHelper):
    """Select Directory"""
    bl_idname = "n2b.select_asset_dir"
    bl_label = "Select Directory"
    filename_ext = ""
    dirpath : bpy.props.StringProperty(name = "", description="Choose directory:", subtype='DIR_PATH')

    settingsType: bpy.props.IntProperty()

    def execute(self, context):
        directory = os.path.dirname(self.filepath)
        if self.settingsType == 0:
            newDir = getPreferences().assetDirs.add()
        elif self.settingsType == 1:
            newDir = getPreferences().assetBlendDirs.add()
        elif self.settingsType == 2:
            newDir = getPreferences().textureDirs.add()
        else:
            print("Invalid settingsType")
            return {'CANCELLED'}
        newDir.directory = directory

        return {'FINISHED'}

class RemoveDirectory(bpy.types.Operator):
    """Remove Directory"""
    bl_idname = "n2b.remove_asset_dir"
    bl_label = "Remove Directory"

    settingsType: bpy.props.IntProperty()
    index : bpy.props.IntProperty()

    def execute(self, context):
        if self.settingsType == 0:
            getPreferences().assetDirs.remove(self.index)
        elif self.settingsType == 1:
            getPreferences().assetBlendDirs.remove(self.index)
        elif self.settingsType == 2:
            getPreferences().textureDirs.remove(self.index)
        else:
            print("Invalid settingsType")
            return {'CANCELLED'}
        return {'FINISHED'}

ArmatureDisplayTypeEnum = [
    ("DEFAULT", "Default", ""),
    ("OCTAHEDRAL", "Octahedral", ""),
    ("STICK", "Stick", ""),
    ("BBONE", "B-Bone", ""),
    ("ENVELOPE", "Envelope", ""),
    ("WIRE", "Wire", "")
]

ShaderParamsFileEnum = [
    ("shader_params.json", "NieR:Automata", ""),
    ("shader_params_bayo3.json", "Bayonetta 3", ""),
]

class N2B2NPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME
    assetDirs: bpy.props.CollectionProperty(type=DirectoryProperty)
    assetBlendDirs: bpy.props.CollectionProperty(type=DirectoryProperty)
    textureDirs: bpy.props.CollectionProperty(type=DirectoryProperty)
    armatureDefaultDisplayType: bpy.props.EnumProperty(name="Armature Display Type", items=ArmatureDisplayTypeEnum, default="DEFAULT")
    armatureDefaultInFront: bpy.props.BoolProperty(name="Armature Default In Front", default=False)
    shaderParamsFile: bpy.props.EnumProperty(name="Shader Parameter Name Source", items=ShaderParamsFileEnum, default="shader_params.json")
    maximizeShaderCompatibility: bpy.props.BoolProperty(name="Maximize Shader Compatibility", default=True, description="Enabling this automatically maximizes shader compatibility by ensuring each mesh has at least 2 UV channels and a color channel.")

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout

        box = layout.box()
        row = box.row()
        row.label(text="Shader Parameter Name Source:")
        row.prop(self, "shaderParamsFile", text="")

        box = layout.box()
        row = box.row()
        row.label(text="Maximize Shader Compatibility:")
        row.prop(self, "maximizeShaderCompatibility", text="")
        drawMultilineLabel(context, self.bl_rna.properties['maximizeShaderCompatibility'].description, box)

        box = layout.box()
        box.label(text="Default Armature Viewport Display Options:")
        row = box.row()
        row.label(text="Display Type:")
        row.prop(self, "armatureDefaultDisplayType", text="")
        row = box.row()
        row.label(text="In Front:")
        row.prop(self, "armatureDefaultInFront", text="")

        # asset dirs selection
        box = layout.box()
        drawMultilineLabel(context, "Assign extracted cpk directories below if you wish to enable bounding box visualization with layout import", box)
        for i, assetDir in enumerate(self.assetDirs):
            row = box.row(align=True)
            row.prop(self.assetDirs[i], "directory", text="")
            remOp = row.operator(RemoveDirectory.bl_idname, text="", icon="X")
            remOp.index = i
            remOp.settingsType = 0
        addOp = box.operator(SelectDirectory.bl_idname, text="Add Directory", icon="FILE_FOLDER")
        addOp.settingsType = 0

        # asset blend dirs selection
        box = layout.box()
        drawMultilineLabel(context, "Assign downloaded blend directories below if you wish to enable full model visualization with layout import", box)
        for i, assetDir in enumerate(self.assetBlendDirs):
            row = box.row(align=True)
            row.prop(self.assetBlendDirs[i], "directory", text="")
            remOp = row.operator(RemoveDirectory.bl_idname, text="", icon="X")
            remOp.index = i
            remOp.settingsType = 1
        addOp = box.operator(SelectDirectory.bl_idname, text="Add Directory", icon="FILE_FOLDER")
        addOp.settingsType = 1

        # asset dirs selection
        box = layout.box()
        drawMultilineLabel(context, "Assign extracted texture directories below for applying textures not included locally in DTT/DAT files", box)
        for i, textureDir in enumerate(self.textureDirs):
            row = box.row(align=True)
            row.prop(self.textureDirs[i], "directory", text="")
            remOp = row.operator(RemoveDirectory.bl_idname, text="", icon="X")
            remOp.index = i
            remOp.settingsType = 2
        addOp = box.operator(SelectDirectory.bl_idname, text="Add Directory", icon="FILE_FOLDER")
        addOp.settingsType = 2


def register():
    bpy.utils.register_class(DirectoryProperty)
    bpy.utils.register_class(SelectDirectory)
    bpy.utils.register_class(RemoveDirectory)
    bpy.utils.register_class(N2B2NPreferences)

def unregister():
    bpy.utils.unregister_class(DirectoryProperty)
    bpy.utils.unregister_class(SelectDirectory)
    bpy.utils.unregister_class(RemoveDirectory)
    bpy.utils.unregister_class(N2B2NPreferences)
